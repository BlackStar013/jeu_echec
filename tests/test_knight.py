import unittest
from src.logique_jeu import *

class TestKnight(unittest.TestCase):

    def test_knight_jumps_over_pieces(self):
        game = Game()

        knight = game.board.get(7, 1)

        moves = knight.valid_moves(game.board)

        self.assertEqual(len(moves), 2)

    def test_knight_capture(self):
        game = Game()
        game.board = Board()

        knight = Knight(Color.WHITE, 4, 4)

        enemy = Pawn(Color.BLACK, 2, 5)

        game.board.set(4, 4, knight)
        game.board.set(2, 5, enemy)

        self.assertIn((2, 5), knight.valid_moves(game.board))