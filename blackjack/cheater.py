#! /u/qaeng/anaconda3/bin/python3
import game
from cards import *

class Cheater(GameStrategy):
    def hit(self, hand):
        try:
            theoretical_hand = Hand( *hand.cards, self.player.table.deck[-1] )
            if not theoretical_hand.is_bust():
                return True
            else:
                return False
        except:
            return False

    def split(self, hand):
        if hand.cards[0].rank == 8 or hand.cards[0].rank == 'A':
            return True

class Super_Cheater(GameStrategy):
    def hit(self, hand):
        try:
            theoretical_hand = Hand( *hand.cards, self.player.table.deck[-1] )
            for x in range(25):
                if theoretical_hand.is_bust():
                    self.player.table.get_card()
                    theoretical_hand = Hand( *hand.cards, self.player.table.deck[-1] )
            if not theoretical_hand.is_bust():
                return True
            else:
                return False
        except:
            return False

    def split(self, hand):
        if hand.cards[0].rank == 8 or hand.cards[0].rank == 'A':
            return True


if __name__ == '__main__':
    game.run_game( Cheater )
    #game.run_game( Super_Cheater )
