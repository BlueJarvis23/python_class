#! /u/qaeng/anaconda3/bin/python3

from cards import *

def run_game( game_strategy=GameStrategy, betting_strategy=Flat_Bet ):
    table = Table(6)
    p = Player( table, betting_strategy, game_strategy )
    d = Player( table, Flat_Bet, GameStrategy )
    #d = Player( table, Flat_Bet, DealerStrategy )
    table.add_player(p)
    table.add_dealer(d)

    win_rate = []

    for y in range(100):
        for x in range(100):
            print("Trick Number: %s" % (x,))
            table.play()

        win_rate.append(table.player.win / (table.player.win + table.player.loss)) 
        print( "Win Rate: %s" % (win_rate,))

    print()
    print( "Average Win Rate: %s" % (sum(win_rate) / float(len(win_rate))))

