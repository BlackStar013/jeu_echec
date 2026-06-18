import unittest
from src.logique_jeu import Game, Board, Tower, King, Color


class TestSetup(unittest.TestCase):

    def test_initial_position(self):
        game = Game()

        self.assertIsInstance(game.board.get(0, 0), Tower)
        self.assertIsInstance(game.board.get(0, 4), King)

        self.assertIsInstance(game.board.get(7, 4), King)

        self.assertEqual(game.board.get(0, 4).color, Color.BLACK)
        self.assertEqual(game.board.get(7, 4).color, Color.WHITE)
