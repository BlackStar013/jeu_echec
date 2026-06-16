import unittest
from src.logique_jeu import *


class TestPawn(unittest.TestCase):

    def test_white_pawn_initial_move(self):
        game = Game()

        pawn = game.board.get(6, 0)

        moves = pawn.valid_moves(game.board)

        self.assertEqual(len(moves), 2)

    def test_black_pawn_initial_move(self):
        game = Game()

        pawn = game.board.get(1, 0)

        moves = pawn.valid_moves(game.board)

        self.assertEqual(len(moves), 2)

    def test_pawn_blocked(self):
        game = Game()

        game.board.set(5, 0, Pawn(Color.BLACK, 5, 0))

        pawn = game.board.get(6, 0)

        self.assertEqual(pawn.valid_moves(game.board), [])

    def test_pawn_capture(self):
        game = Game()
        game.board = Board()

        white = Pawn(Color.WHITE, 4, 4)
        black = Pawn(Color.BLACK, 3, 5)

        game.board.set(4, 4, white)
        game.board.set(3, 5, black)

        moves = white.valid_moves(game.board)

        self.assertIn((3, 5), moves)