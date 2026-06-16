import unittest
from src.logique_jeu import *

class TestRook(unittest.TestCase):

    def test_rook_free_lines(self):
        game = Game()
        game.board = Board()

        rook = Tower(Color.WHITE, 4, 4)

        game.board.set(4, 4, rook)

        moves = rook.valid_moves(game.board)

        self.assertIn((0, 4), moves)
        self.assertIn((7, 4), moves)

    def test_rook_capture(self):
        game = Game()
        game.board = Board()

        rook = Tower(Color.WHITE, 4, 4)

        enemy = Pawn(Color.BLACK, 1, 4)

        game.board.set(4, 4, rook)
        game.board.set(1, 4, enemy)

        self.assertIn((1, 4), rook.valid_moves(game.board))