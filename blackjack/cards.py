#! /usr/local/bin/python3

import random

class Suit:
    def __init__( self, name, symbol ):
        self.name = name
        self.symbol = symbol
    def __str__(self):
        return "{symbol}".format(**self.__dict__)
    def __repr__(self):
        return "{__class__.__name__}(name={name!r}, symbol={symbol!r})".format(__class__=self.__class__, **self.__dict__)

class Card:
    def __init__( self, rank, suit ):
        self.rank = rank
        self.suit = suit
        self.hard, self.soft = self._points()
    def __str__(self):
        return "| {rank} {suit} |".format(**self.__dict__)
    def __repr__(self):
        return "{__class__.__name__}(rank={rank!r}, suit={suit!r})".format(__class__=self.__class__, **self.__dict__)
class AceCard(Card):
    def _points(self):
        return 1, 11
class FaceCard(Card):
    def _points(self):
        return 10, 10
class NumberCard(Card):
    def _points(self):
        return int(self.rank), int(self.rank)

def init_card( rank, suit ):
    if rank == 1:
        return AceCard( 'A' , suit )
    elif 2 <= rank and rank < 11:
        return NumberCard( rank, suit )
    elif 11 <= rank and rank < 14:
        name = {11: 'J', 12: 'Q', 13: 'K'}
        return FaceCard( name[rank], suit )
    else:
        raise Exception( "Card Rank out of Range")

class Hand:
    def __init__(self, *args):
        if not all(isinstance(x, Card) for x in args):
            raise Exception( "Hands may only contain Cards" )
        self.cards = list(args)
        self.update_counts()
        self.is_bust()
    def __str__(self):
        return "{cards}".format(**self.__dict__)
    def __repr__(self):
        return "{__class__.__name__}(cards={cards!r})".format(__class__=self.__class__, **self.__dict__)
    def add_card(self, card):
        if not isinstance(card, Card):
            raise Exception( "Only Cards may be added to a Hand" )
        self.cards.append(card)
        self.update_counts()
        self.is_bust()
    def update_counts(self):
        self.hard_count = sum(c.hard for c in self.cards)
        self.soft_count = sum(c.soft for c in self.cards)
    def score(self):
        if self.hard_count > 21:
            return 0
        elif self.soft_count > 21:
            return self.hard_count
        elif self.soft_count <= 21 and self.hard_count <= 21:
            return max( self.soft_count, self.hard_count )
    def is_bust(self):
        self.bust = True if self.hard_count > 21 else False
        return self.bust
    def split(self, split_num ):
        pass

class Deck(list):
    def __init__(self, num_decks=1):
        super().__init__(init_card(rank, suit) for rank in range(1,14) for suit in (Club, Diamond, Spade, Heart) for d in range(num_decks))
        random.shuffle( self ) 
    ## Possible Burn function here

class Player:
    # Player has 1 or many hands
    # Player has a gamestrategy
    # Player has a bettingstrategy
    # Player has a table
    def __init__(self, table, bet_strategy, game_strategy, **kwargs):
        self.table = table
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.hands = []
        self.loss = 0
        self.win = 0
        self.pool = 100
        self.__dict__.update( kwargs )
    def play( self ):
        self.pool = self.pool - self.bet_strategy.bet()
        if not self.hands: # is Dealer
            self.table.place_bet( self.bet_strategy.bet() )
            self.hands.append( self.table.get_hand() ) ## used later in splitting hands...
        for hand in self.hands:
            while self.game_strategy.hit(hand):
                hand.add_card( self.table.get_card() )
    def end_trick(self):
        self.hands = []
    def add_pool(self, amount):
        self.pool = self.pool + amount

class GameStrategy:
    def insurance( self, hand ):
        return False
    def split( self, hand ):
        return False
    def double( self, hand ):
        return False
    def hit( self, hand ):
        return sum(c.hard for c in hand.cards) <= 17

class DealerStrategy(GameStrategy):
    def hit(self, hand):
        for player in self.table.players:
            for hand in player.hands:
                if not hand.is_bust():
                    return True
        return False

class BettingStrategy:
    def bet( self ):
        raise NotImplementedError( "No bet method" )
    def record_win( self ):
        pass
    def record_loss( self ):
        pass

class Flat_Bet(BettingStrategy):
    def bet(self):
        return 1

class Table:
#    def __init__(self, num_decks=1):
#        self.deck = Deck(num_decks)
#        self.dealer = Player( self, bet_strategy, game_strategy )
    # Table has one Dealer
    # 1 or many Players
    # 1 Deck
    def __init__( self, num_decks=1 ):
        self.num_decks = num_decks
        self.deck = Deck(num_decks)
        self.players = []
        self.pot = 0
    def place_bet( self, amount ):
        self.pot = self.pot + (amount*2) # Dealer just matches bet
    def get_hand(self):
        try:
            h = Hand(self.deck.pop(), self.deck.pop())
#            print( "Deal: %s" % (h,))
            return h
        except IndexError:
            self.deck = Deck(self.num_decks)
            return self.get_hand()
    def get_card(self):
        try:
            c = self.deck.pop()
            return c
        except:
            self.deck = Deck(self.num_decks)
            return self.get_card()   
    def add_player(self, player):
        self.players.append( player )
    def add_dealer(self, dealer):
        self.dealer = dealer
    def play(self):
        self.dealer.hands.append( self.get_hand() )

        for player in self.players:
            print( "Player Pool: %s" % (player.pool) )
            player.play()

        for player in self.players:
#            print("%s" % (list(map( lambda x: x.is_bust(), player.hands),)))
            if False in map( lambda x: x.is_bust(), player.hands):
                print("\tDealer Play -- ")
                self.dealer.play()
                break

        for player in self.players:
            for hand in player.hands:
                if hand.score() > self.dealer.hands[0].score():
                    print("\tPlayer won this trick.")
                    player.win = player.win + 1
                    player.add_pool(self.pot)
                elif hand.score() == self.dealer.hands[0].score():
                    print("\tTie! No Scores")
                    pass
                else:
                    player.loss = player.loss + 1

        for player in self.players:
            print("\tPlayer Score: %s, Hand: %s" % (player.hands[0].score(), ', '.join(map(str, player.hands[0].cards))))
            #print("\tPlayer Score: %s" % (player.hands[0].score(),))
        if self.dealer.hands:
            print("\tDealer Score: %s, Hand: %s" % (self.dealer.hands[0].score(), ', '.join(map(str, self.dealer.hands[0].cards))))
            #print("\tDealer Score: %s" % (self.dealer.hands[0].score(),))

        for player in self.players:
            player.end_trick()
        self.dealer.end_trick()
        self.pot = 0
                    
            
    

Club, Diamond, Spade, Heart = Suit('Club', '\u2667'), Suit('Diamond', '\u25C6'), Suit('Spade', '\u2664'), Suit('Heart', '\u2665')

#deck = [init_card(rank, suit) for rank in range(1,14) for suit in (Club, Diamond, Spade, Heart)]
#
#random.shuffle(deck)
#
#for x in deck:
#    print(x)
#print(deck)
#
#print( Club, Diamond, Spade, Heart )
#
#print(', '.join(map(str,deck)))
#
#h1 = Hand(deck.pop(), deck.pop())
#h2 = Hand(deck.pop(), deck.pop())
#
#print( ', '.join(map(str, h1.cards)))
#print( ', '.join(map(str, h2.cards)))









