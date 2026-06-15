import unittest
from src.logique_jeu import Game


class TestMoves(unittest.TestCase):

    def test_move_piece(self):
        game = Game()
        pawn = game.board.get(6, 4)

        self.assertTrue(game.move_piece(pawn, 4, 4))
        self.assertIsNone(game.board.get(6, 4))
        self.assertEqual(game.board.get(4, 4), pawn)

    def test_illegal_move(self):
        game = Game()
        pawn = game.board.get(6, 4)

        self.assertFalse(game.move_piece(pawn, 3, 4))
