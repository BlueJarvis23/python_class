
from cards import *
table = Table(6)
flat_bet = Flat_Bet()
dumb = GameStrategy()
p = Player( table, flat_bet, dumb )
#d = Dealer( table, flat_bet, dumb )
for x in range(100):
    p.play()
    p.end_trick()
    print()
    print( p.win, p.loss )

