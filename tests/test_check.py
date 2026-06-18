import unittest
from src.logique_jeu import *

class TestCheck(unittest.TestCase):

    def test_not_in_check(self):
        game = Game()

        self.assertFalse(game.is_in_check(Color.WHITE))
        self.assertFalse(game.is_in_check(Color.BLACK))

    def test_rook_check(self):
        game = Game()
        game.board = Board()

        white_king = King(Color.WHITE, 7, 4)
        black_rook = Tower(Color.BLACK, 0, 4)

        game.board.set(7, 4, white_king)
        game.board.set(0, 4, black_rook)

        self.assertTrue(game.is_in_check(Color.WHITE))