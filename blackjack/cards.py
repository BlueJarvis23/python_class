
class Suit:
    def __init__( self, name, symbol ):
        self.name = name
        self.symbol = symbol

class Card:
    def __init__( self, rank, suit ):
        self.rank = rank
        self.suit = suit
        self.hard, self.soft = self._points()
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

Club, Diamond, Heart, Spade = Suit('Club', '+'), Suit('Diamond', '+'), Suit('Spade', '='), Suit('Heart', '=')
deck = [init_card(rank, suit) for rank in range(1,14) for suit in (Club, Diamond, Heart, Spade)]

print(deck)
