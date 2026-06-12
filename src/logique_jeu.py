from enum import Enum
from copy import deepcopy


# création d'enums pour être plus clair dans le lien entre valeur (id et autre) et leur sens
class Color(Enum):
    WHITE = 0
    BLACK = 1


class GameState(Enum):
    RUNNING = 0
    CHECK = 1
    CHECKMATE = 2
    STALEMATE = 3


class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False

    def enemy(self):
        if self.color == Color.WHITE:
            return Color.BLACK
        return Color.WHITE

    def valid_moves(self, board):
        raise NotImplementedError


class Pawn(Piece):
    def valid_moves(self, board):
        moves = []
        direction = -1 if self.color == Color.WHITE else 1
        start_row = 6 if self.color == Color.WHITE else 1
        # avance de 1
        r = self.row + direction
        if board.inside(r, self.col) and board.get(r, self.col) is None:
            moves.append((r, self.col))
        # avance de 2
        r2 = self.row + 2 * direction
        # on vérifie qu'il n'a pas encore bougé, que la case devant et la case d'arrivée sont vides (dans le plateau) 
        if (self.row == start_row and board.get(r, self.col) is None and board.inside(r2, self.col) and board.get(r2, self.col) is None):
            moves.append((r2, self.col))
        # captures
        for dc in (-1, 1):
            c = self.col + dc
            if board.inside(r, c):
                target = board.get(r, c)
                if( (target is not None) and (target.color != self.color) ):
                    moves.append((r, c))
        return moves


class Knight(Piece):
    def valid_moves(self, board):
        moves = []
        offsets = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),]
        for dr, dc in offsets:
            r = self.row + dr
            c = self.col + dc
            if not board.inside(r, c):
                continue
            target = board.get(r, c)
            if( (target is None) or (target.color != self.color) ):
                moves.append((r, c))
        return moves


class SlidingPiece(Piece):
    # fonction factorisée pour les pièces avec un mouvement glissant, donc les tours, les fous, et la reine
    DIRECTIONS = []
    def valid_moves(self, board):
        moves = []
        for dr, dc in self.DIRECTIONS:
            r = self.row + dr
            c = self.col + dc
            while board.inside(r, c):
                target = board.get(r, c)
                if target is None:
                    moves.append((r, c))
                else:
                    if target.color != self.color:
                        moves.append((r, c))
                    break
                r += dr
                c += dc
        return moves


class Bishop(SlidingPiece): # fou en anglais
    DIRECTIONS = [
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)]


class Tower(SlidingPiece):
    DIRECTIONS = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)]


class Queen(SlidingPiece):
    DIRECTIONS = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)]


class King(Piece):
    def valid_moves(self, board):
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if( (dr == 0) and (dc == 0) ):
                    continue
                r = self.row + dr
                c = self.col + dc
                if not board.inside(r, c):
                    continue
                target = board.get(r, c)
                if ( (target is None) or (target.color != self.color) ):
                    moves.append((r, c))
        return moves


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
    def inside(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    def get(self, row, col):
        return self.grid[row][col]
    def set(self, row, col, piece):
        self.grid[row][col] = piece
        if piece:
            piece.row = row
            piece.col = col


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = Color.WHITE
        self.state = GameState.RUNNING
        self.setup()
    def setup(self):
        # noirs
        order = [
            Tower,
            Knight,
            Bishop,
            Queen,
            King,
            Bishop,
            Knight,
            Tower]
        for col, piece_class in enumerate(order):
            self.board.set(0,col,piece_class(Color.BLACK, 0, col))
        for col in range(8):
            self.board.set(1,col,Pawn(Color.BLACK, 1, col))
        # blancs
        for col in range(8):
            self.board.set(6,col,Pawn(Color.WHITE, 6, col))
        for col, piece_class in enumerate(order):
            self.board.set(7,col,piece_class(Color.WHITE, 7, col))
    def find_king(self, color):
        for row in self.board.grid:
            for piece in row:
                if ( (isinstance(piece, King)) and (piece.color == color)):
                    return piece
        return None

    def is_in_check(self, color):
        king = self.find_king(color)
        for row in self.board.grid:
            for piece in row:
                if( (piece is not None) and (piece.color != color) ):
                    if(king.row,king.col) in piece.valid_moves(self.board):
                        return True
        return False

    def simulate_move(self, piece, dest_row, dest_col):
        game_copy = deepcopy(self)
        copied_piece = game_copy.board.get(piece.row, piece.col)
        game_copy.move_piece(copied_piece, dest_row, dest_col, validate=False)
        return game_copy

    def legal_moves(self, piece):
        legal = []
        for row, col in piece.valid_moves(self.board):
            sim = self.simulate_move(piece, row, col)
            if not sim.is_in_check(piece.color):
                legal.append((row, col))
        return legal

    def move_piece(self, piece, row, col, validate=True):
        if validate:
            if (row, col) not in self.legal_moves(piece):
                return False
        self.board.set(piece.row, piece.col, None)
        self.board.set(row, col, piece)
        piece.has_moved = True
        return True

    def all_moves(self, color):
        moves = []
        for row in self.board.grid:
            for piece in row:
                if( (piece is not None) and (piece.color == color)):
                    moves.extend(self.legal_moves(piece))
        return moves

    def next_turn(self):
        self.turn = (Color.BLACK if self.turn == Color.WHITE else Color.WHITE)
        enemy = self.turn
        if(self.is_in_check(enemy)):
            if(not self.all_moves(enemy)):
                self.state = GameState.CHECKMATE
            else:
                self.state = GameState.CHECK
        else:
            if(not self.all_moves(enemy)):
                self.state = GameState.STALEMATE
            else:
                self.state = GameState.RUNNING
