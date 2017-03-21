
from cards import *
table = Table(6)
flat_bet = Flat_Bet()
dumb = GameStrategy()
#dealer_strat = DealerStrategy()
p = Player( table, flat_bet, dumb )
d = Player( table, flat_bet, dumb )
#d = Player( table, flat_bet, dealer_strat )
table.add_player(p)
table.add_dealer(d)

for x in range(200):
    print("Trick Number: %s" % (x,))
    table.play()

for player in table.players:
    print( "Player Pool: %s" % (player.pool) )
    print( "Win Rate: %s" % (player.win / (player.win + player.loss),) )

