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
        # pour une avance simple de 1 case
        r = self.row + direction
        if(board.inside(r, self.col) and board.get(r, self.col) is None):
            moves.append((r, self.col))
        # pour l'avance de deux
        r2 = self.row + 2 * direction
        if( (self.row == start_row and board.inside(r2, self.col) and board.get(r, self.col) is None and board.get(r2, self.col) is None) ):
            moves.append((r2, self.col))
        # pour manger de manière classique
        for dc in (-1, 1):
            c = self.col + dc
            if( board.inside(r, c)):
                target = board.get(r, c)
                if( target is not None and target.color != self.color):
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
                    if( target.color != self.color):
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
                if( dr == 0 and dc == 0):
                    continue
                r = self.row + dr
                c = self.col + dc
                if( not board.inside(r, c)):
                    continue
                target = board.get(r, c)
                if( target is None or target.color != self.color):
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
        self.en_passant_target = None
        self.move_history = []
    
    def setup(self):
        # noirs
        order = [Tower, Knight, Bishop, Queen, King, Bishop, Knight, Tower]
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
                if( (isinstance(piece, King)) and (piece.color == color)):
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
        moves = piece.valid_moves(self.board)
        # pour la prise en passant, donc seulement pour les pions
        if(isinstance(piece, Pawn)):
            if(self.en_passant_target is not None):
                ep_row, ep_col = self.en_passant_target
                direction = -1 if piece.color == Color.WHITE else 1
                if(ep_row == piece.row + direction and abs(ep_col - piece.col) == 1):
                    moves.append((ep_row, ep_col))
        # pour le roque, on différencie en petit et grand
        if(isinstance(piece, King) and not piece.has_moved):
            row = piece.row
            # donc le petit
            rook = self.board.get(row, 7)
            if((isinstance(rook, Tower) and not rook.has_moved and self.board.get(row, 5) is None and self.board.get(row, 6) is None)):
                enemy = piece.enemy()
                if((not self.square_attacked(row, 4, enemy) and not self.square_attacked(row, 5, enemy) and not self.square_attacked(row, 6, enemy))):
                    moves.append((row, 6))
            # et le 3 cases
            rook = self.board.get(row, 0)
            if( (isinstance(rook, Tower) and not rook.has_moved and self.board.get(row, 1) is None and self.board.get(row, 2) is None and self.board.get(row, 3) is None)):
                enemy = piece.enemy()
                if( (not self.square_attacked(row, 4, enemy) and not self.square_attacked(row, 3, enemy) and not self.square_attacked(row, 2, enemy))):
                    moves.append((row, 2))
        # les autres coups classiques
        for row, col in moves:
            sim = self.simulate_move(piece, row, col)
            if( not sim.is_in_check(piece.color)):
                legal.append((row, col))
        return legal

    def square_attacked(self, row, col, by_color):
        for board_row in self.board.grid:
            for piece in board_row:
                if(piece is None or piece.color != by_color):
                    continue
                if(isinstance(piece, Pawn)):
                    direction = -1 if piece.color == Color.WHITE else 1
                    for dc in (-1, 1):
                        if((piece.row + direction, piece.col + dc) == (row, col)):
                            return True
                else:
                    if((row, col) in piece.valid_moves(self.board)):
                        return True
        return False

    def move_piece(self, piece, row, col, validate=True):
        if validate:
            if( (row, col) not in self.legal_moves(piece)):
                return False
        old_row = piece.row
        old_col = piece.col
        captured_piece = self.board.get(row, col)
        # donc la prise en passant
        if isinstance(piece, Pawn):
            if( (self.en_passant_target is not None and (row, col) == self.en_passant_target and self.board.get(row, col) is None)):
                captured_row = old_row
                captured_col = col
                self.board.set(captured_row, captured_col, None)
        # le roque
        if isinstance(piece, King):
            # petit
            if(col - old_col == 2):
                rook = self.board.get(old_row, 7)
                self.board.set(old_row, 7, None)
                self.board.set(old_row, 5, rook)
            # et grand
            elif(col - old_col == -2):
                rook = self.board.get(old_row, 0)
                self.board.set(old_row, 0, None)
                self.board.set(old_row, 3, rook)
        # le reste
        self.board.set(old_row, old_col, None)
        self.board.set(row, col, piece)
        # et on change les cases de prise en passant
        self.en_passant_target = None
        if(isinstance(piece, Pawn)):
            if(abs(row - old_row) == 2):
                middle_row = (row + old_row) // 2
                self.en_passant_target = (middle_row, col)
        # et la promotion des pions
        if(isinstance(piece, Pawn)):
            if(row == 0 or row == 7):
                self.board.set(row, col, Queen(piece.color, row, col))
        piece.has_moved = True
        start = self.square_name(old_row, old_col)
        end = self.square_name(row, col)

        piece_name = piece.__class__.__name__

        move_text = (
            f"{piece_name} : "
            f"{start} -> {end}"
        )

        if captured_piece is not None:
            move_text += " (capture)"

        self.move_history.append(move_text)
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
    
    def square_name(self, row, col):
        file = chr(ord('a') + col)
        rank = str(8 - row)
        return file + rank