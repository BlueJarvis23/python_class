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
    def add_card(self, card):
        if not isinstance(card, Card):
            raise Exception( "Only Cards may be added to a Hand" )
        self.cards.append(card)
        self.update_counts()
        self.is_bust()
    def update_counts(self):
        self.hard_count = sum(c.hard for c in self.cards)
        self.soft_count = sum(c.soft for c in self.cards)
    def is_bust(self):
        self.bust = False if self.soft_count > 21 else True

class Player:
    # Player has 1 or many hands
    # Player has a strategy
    pass

class Strategy:
    pass

class Table:
    # Table has one Dealer
    # 1 or many Players
    # 1 Deck
    pass


Club, Diamond, Spade, Heart = Suit('Club', '\u2667'), Suit('Diamond', '\u25C6'), Suit('Spade', '\u2664'), Suit('Heart', '\u2665')
deck = [init_card(rank, suit) for rank in range(1,14) for suit in (Club, Diamond, Spade, Heart)]

random.shuffle(deck)

for x in deck:
    print(x)
print(deck)

print( Club, Diamond, Spade, Heart )

print(', '.join(map(str,deck)))

h1 = Hand(deck.pop(), deck.pop())
h2 = Hand(deck.pop(), deck.pop())

print( ', '.join(map(str, h1.cards)))
print( ', '.join(map(str, h2.cards)))











