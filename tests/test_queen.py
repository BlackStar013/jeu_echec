import unittest
from src.logique_jeu import *

class TestQueen(unittest.TestCase):

    def test_queen_moves(self):
        game = Game()
        game.board = Board()

        queen = Queen(Color.WHITE, 4, 4)

        game.board.set(4, 4, queen)

        moves = queen.valid_moves(game.board)

        self.assertIn((4, 0), moves)
        self.assertIn((0, 4), moves)
        self.assertIn((0, 0), moves)