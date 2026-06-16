import unittest
from src.logique_jeu import *

class TestKing(unittest.TestCase):

    def test_king_moves(self):
        game = Game()
        game.board = Board()

        king = King(Color.WHITE, 4, 4)

        game.board.set(4, 4, king)

        moves = king.valid_moves(game.board)

        self.assertEqual(len(moves), 8)

    def test_king_corner(self):
        game = Game()
        game.board = Board()

        king = King(Color.WHITE, 0, 0)

        game.board.set(0, 0, king)

        moves = king.valid_moves(game.board)

        self.assertEqual(len(moves), 3)