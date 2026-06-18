import unittest
from src.logique_jeu import (
    Game, Board, Color,
    Pawn, King, Tower,
    Queen, GameState
)


class TestRules(unittest.TestCase):

    def test_check_detection(self):
        game = Game()
        game.board = Board()

        white_king = King(Color.WHITE, 7, 4)
        black_rook = Tower(Color.BLACK, 0, 4)

        game.board.set(7, 4, white_king)
        game.board.set(0, 4, black_rook)

        self.assertTrue(game.is_in_check(Color.WHITE))

    def test_castling_available(self):
        game = Game()

        game.board.set(7, 5, None)
        game.board.set(7, 6, None)

        king = game.board.get(7, 4)

        self.assertIn((7, 6), game.legal_moves(king))

    def test_en_passant(self):
        game = Game()
        game.board = Board()

        white_king = King(Color.WHITE, 7, 4)
        black_king = King(Color.BLACK, 0, 4)

        white_pawn = Pawn(Color.WHITE, 3, 4)
        black_pawn = Pawn(Color.BLACK, 1, 5)

        game.board.set(7, 4, white_king)
        game.board.set(0, 4, black_king)

        game.board.set(3, 4, white_pawn)
        game.board.set(1, 5, black_pawn)

        game.move_piece(black_pawn, 3, 5, validate=False)

        self.assertIn((2, 5), game.legal_moves(white_pawn))

    def test_promotion(self):
        game = Game()
        game.board = Board()

        white_king = King(Color.WHITE, 7, 4)
        black_king = King(Color.BLACK, 0, 4)

        pawn = Pawn(Color.WHITE, 1, 0)

        game.board.set(7, 4, white_king)
        game.board.set(0, 4, black_king)
        game.board.set(1, 0, pawn)

        game.move_piece(pawn, 0, 0, validate=False)

        self.assertIsInstance(game.board.get(0, 0), Queen)

    def test_checkmate(self):
        game = Game()

        game.move_piece(game.board.get(6, 5), 5, 5)
        game.next_turn()

        game.move_piece(game.board.get(1, 4), 3, 4)
        game.next_turn()

        game.move_piece(game.board.get(6, 6), 4, 6)
        game.next_turn()

        game.move_piece(game.board.get(0, 3), 4, 7)
        game.next_turn()

        self.assertEqual(game.state, GameState.CHECKMATE)