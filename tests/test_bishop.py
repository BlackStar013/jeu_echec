import unittest
from src.logique_jeu import *

class TestBishop(unittest.TestCase):

    def test_bishop_free_diagonal(self):
        game = Game()
        game.board = Board()

        bishop = Bishop(Color.WHITE, 4, 4)

        game.board.set(4, 4, bishop)

        moves = bishop.valid_moves(game.board)

        self.assertIn((0, 0), moves)
        self.assertIn((7, 7), moves)

    def test_bishop_blocked(self):
        game = Game()
        game.board = Board()

        bishop = Bishop(Color.WHITE, 4, 4)

        blocker = Pawn(Color.WHITE, 5, 5)

        game.board.set(4, 4, bishop)
        game.board.set(5, 5, blocker)

        self.assertNotIn((6, 6), bishop.valid_moves(game.board))