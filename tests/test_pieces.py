import unittest
from src.logique_jeu import Game


class TestPieces(unittest.TestCase):

    def test_white_pawn_moves(self):
        game = Game()
        pawn = game.board.get(6, 4)

        moves = pawn.valid_moves(game.board)

        self.assertIn((5, 4), moves)
        self.assertIn((4, 4), moves)

    def test_black_pawn_moves(self):
        game = Game()
        pawn = game.board.get(1, 4)

        moves = pawn.valid_moves(game.board)

        self.assertIn((2, 4), moves)
        self.assertIn((3, 4), moves)

    def test_knight_moves(self):
        game = Game()
        knight = game.board.get(7, 1)

        moves = knight.valid_moves(game.board)

        self.assertIn((5, 0), moves)
        self.assertIn((5, 2), moves)
