import unittest
from src.logique_jeu import *

class TestCastling(unittest.TestCase):

    def test_kingside_castling(self):
        game = Game()

        game.board.set(7, 5, None)
        game.board.set(7, 6, None)

        king = game.board.get(7, 4)

        self.assertIn((7, 6), game.legal_moves(king))

    def test_castling_forbidden_if_king_moved(self):
        game = Game()

        game.board.set(7, 5, None)
        game.board.set(7, 6, None)

        king = game.board.get(7, 4)
        king.has_moved = True

        self.assertNotIn((7, 6), game.legal_moves(king))