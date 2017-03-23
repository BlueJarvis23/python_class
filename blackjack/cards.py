#! /usr/local/bin/python3

import random
import copy

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
        self.pot = 0
    def __str__(self):
        return ' '.join(map(str, self.cards))
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
        return True if self.hard_count > 21 else False
    def split_hand(self):
        extra_card = self.cards.pop()
        return Hand(extra_card)
    def splitable(self):
        if len(self.cards) == 2 and len(set(map(lambda x: x.rank, self.cards))) == 1:
            return True
        return False
    def double_downable(self):
        if len(self.cards) == 2: 
            return True
        return False
    def place_bet( self, amount ):
        self.pot = self.pot + (amount*2) # Dealer just matches bet

class Deck(list):
    def __init__(self, num_decks=1):
        super().__init__(init_card(rank, suit) for rank in range(1,14) for suit in (Club, Diamond, Spade, Heart) for d in range(num_decks))
        random.shuffle( self ) 
    ## Possible Burn function here

class Player:
    def __init__(self, table, bet_strategy, game_strategy, **kwargs):
        self.table = table
        self.bet_strategy = bet_strategy(self)
        self.game_strategy = game_strategy(self)
        self.hands = []
        self.loss = 0
        self.win = 0
        self.pool = 100
        self.last_bet = 0
        self.__dict__.update( kwargs )
    def __str__(self):
        return ' -- '.join(map(str, self.hands))
        return "{hands}".format(**self.__dict__)
    def __repr__(self):
        return "{__class__.__name__}(hands={hands!r})".format(__class__=self.__class__, **self.__dict__)
    def play( self ):
        if not self.hands: # is Dealer
            self.hands.append( self.table.get_hand() ) ## used later in splitting hands...
            self.hands[0].place_bet( self.place_bet( self.bet_strategy.bet() ))

# Double Down
        for hand in self.hands:
            if self.game_strategy.DD(hand):
                hand.place_bet( self.place_bet( self.last_bet ) )
                hand.add_card( self.table.get_card() )
                print("\t\tDouble Down")
# Split
        for hand in self.hands:
            if self.game_strategy.SPLT(hand):
                hand.place_bet( self.place_bet( self.last_bet ) )
                self.hands.append( hand.split_hand() )
                print("\t\tSplit")
# Hit
        for hand in self.hands:
            while self.game_strategy.HIT(hand):
                hand.add_card( self.table.get_card() )

    def end_trick(self):
        self.hands = []
    def add_pool(self, amount):
        self.pool = self.pool + amount
    def place_bet(self, amount):
        self.last_bet = amount
        self.pool = self.pool - amount
        return amount

class GameStrategy:
    def __init__(self, player):
        self.player = player
    def DD( self, hand ):
        if hand.double_downable():
            return self.double_down( hand )
        return False
    def SPLT( self, hand ):
        if hand.splitable():
            return self.split( hand )
        return False
    def HIT( self, hand):
        if not hand.is_bust():
            return self.hit( hand )
        return False

## Only Over Ride These ##
    def double_down( self, hand ):
        return False 
    def split( self, hand ):
        return False 
    def hit( self, hand ):
        return sum(c.hard for c in hand.cards) < 17
## Only Over Ride These ##

class DealerStrategy(GameStrategy):
    def hit(self, hand):
        for h in self.player.table.player.hands:
            if not h.is_bust() and not hand.is_bust() and hand.score() < h.score():
                return True
        return False

class BettingStrategy:
    def __init__(self, player):
        self.player = player
    def bet( self ):
        raise NotImplementedError( "No bet method" )

class Flat_Bet(BettingStrategy):
    def bet(self):
        return 1

class Table:
    def __init__( self, num_decks=1 ):
        self.num_decks = num_decks
        self.deck = Deck(num_decks)
    def get_hand(self):
        try:
            h = Hand(self.deck.pop(), self.deck.pop())
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
        self.player = player
    def add_dealer(self, dealer):
        self.dealer = dealer
    def get_dealer_visible_card(self):
        return copy.deepcopy( self.dealer.hands[0].cards[0] )
    def play(self):
        self.dealer.hands.append( self.get_hand() )

        print("\tDealer Card: %s" % (self.get_dealer_visible_card()))
        self.player.play()

        if False in map( lambda x: x.is_bust(), self.player.hands):
            print("\tDealer Play")
            self.dealer.play()

        for hand in self.player.hands:
            if hand.score() > self.dealer.hands[0].score():
                print("\tPlayer won this trick.")
                self.player.win = self.player.win + 1
                self.player.add_pool(hand.pot)
            elif hand.score() == self.dealer.hands[0].score():
                print("\tTie! No Scores")
                self.player.add_pool(hand.pot / 2)
                pass
            else:
                self.player.loss = self.player.loss + 1

        print("\tPlayer Score: %s, Player Pool: %s, Player: %s" % (', '.join(map(lambda x: str(x.score()),  self.player.hands)), self.player.pool, self.player ))
        if self.dealer.hands:
            print("\tDealer Score: %s, Dealer: %s" % (', '.join(map(lambda x: str(x.score()), self.dealer.hands)), self.dealer ))

        self.player.end_trick()
        self.dealer.end_trick()
        self.pot = 0
                    
    

Club, Diamond, Spade, Heart = Suit('Club', '\u2667'), Suit('Diamond', '\u25C6'), Suit('Spade', '\u2664'), Suit('Heart', '\u2665')

