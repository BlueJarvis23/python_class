#! /u/qaeng/anaconda3/bin/python3
import game
from cards import *

class inclass_strat(GameStrategy):
    def double_down( self, hand ):
        return False 
    def split( self, hand ):
        return False 
    def hit( self, hand ):
        ## Dealver Visible Card
        dc = self.player.table.get_dealer_visible_card()
        if dc.hard >= 2 and dc.hard <= 7:
            if hand.score() >=17:
                return False 
            else:
                return True 
        else:
            return True

game.run_game( inclass_strat )

