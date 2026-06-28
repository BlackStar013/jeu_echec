import pygame
import json

from logique_jeu import (
    Game,
    Color,
    Pawn,
    Tower,
    Knight,
    Bishop,
    Queen,
    King,
    GameState)


class GameManager:
    TILE_SIZE = 80
    COLORS = {"light": (240, 217, 181),
        "dark": (181, 136, 99),
        "selected": (255, 255, 0),
        "move": (0, 200, 0),}
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))
        pygame.display.set_caption("Jeu d'échecs")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.selected_piece = None
        self.available_moves = []
        self.running = True
        self.iso_tile_width = 80
        self.iso_tile_height = 40
        self.origin_x = 320
        self.origin_y = 100
    
    def board_to_iso(self, row, col):
        x = (col - row) * (self.iso_tile_width // 2)
        y = (col + row) * (self.iso_tile_height // 2)
        return (self.origin_x + x, self.origin_y + y)
    
    def iso_to_board(self, x, y):
        x -= self.origin_x
        y -= self.origin_y
        col = (x/(self.iso_tile_width/2) + y/(self.iso_tile_height/2)) / 2
        row = (y/(self.iso_tile_height / 2) - x/(self.iso_tile_width / 2))/2
        return int(round(row)), int(round(col))

    def save_game(self, filename="save.json"):
        data = {"turn": self.game.turn.value, "pieces": [],}
        for row in self.game.board.grid:
            for piece in row:
                if piece is None:
                    continue
                data["pieces"].append({
                    "type": piece.__class__.__name__,
                    "color": piece.color.value,
                    "row": piece.row,
                    "col": piece.col,
                    "has_moved": piece.has_moved})
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print("Partie sauvegardée.")

    def load_game(self, filename="save.json"):
        with open(filename, "r") as file:
            data = json.load(file)
        self.game = Game()
        self.game.board.grid = [[None for _ in range(8)] for _ in range(8)]
        classes = {"Pawn": Pawn, "Tower": Tower, "Knight": Knight, "Bishop": Bishop, "Queen": Queen, "King": King,}
        for p in data["pieces"]:
            color = Color(p["color"])
            piece = classes[p["type"]](color, p["row"], p["col"])
            piece.has_moved = p["has_moved"]
            self.game.board.set(p["row"], p["col"], piece)
        self.game.turn = Color(data["turn"])
        print("Partie chargée.")

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = self.COLORS["light"]
                else:
                    color = self.COLORS["dark"]
                self.draw_iso_tile(row, col, color)

    def draw_iso_tile(self, row, col, color):
        x, y = self.board_to_iso(row, col)
        hw = self.iso_tile_width // 2
        hh = self.iso_tile_height // 2
        points = [(x, y - hh), (x + hw, y), (x, y + hh), (x - hw, y)]
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, (0, 0, 0), points, 1)

    def piece_symbol(self, piece):
        symbols = {
            Color.WHITE: {
                Pawn: "♙",
                Tower: "♖",
                Knight: "♘",
                Bishop: "♗",
                Queen: "♕",
                King: "♔",
            },
            Color.BLACK: {
                Pawn: "♟",
                Tower: "♜",
                Knight: "♞",
                Bishop: "♝",
                Queen: "♛",
                King: "♚",
            }
        }
        return symbols[piece.color][type(piece)]

    def draw_pieces(self):
        font = pygame.font.SysFont("segoeuisymbol", 48)
        pieces_to_draw = []
        for row in self.game.board.grid:
            for piece in row:
                if piece is None:
                    continue
                depth = piece.row + piece.col
                pieces_to_draw.append((depth, piece))
        pieces_to_draw.sort(key=lambda x: x[0])
        for _, piece in pieces_to_draw:
            x, y = self.board_to_iso(piece.row, piece.col)
            symbol = self.piece_symbol(piece)
            if piece.color == Color.WHITE:
                color = (255, 255, 255)
                outline = (0, 0, 0)
            else:
                color = (20, 20, 20)
                outline = (255, 255, 255)
            x, y = self.board_to_iso(piece.row, piece.col)
            text = font.render(symbol, True, color)
            shadow = font.render(symbol, True, outline)
            rect = text.get_rect(center=(x, y - 20))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.screen.blit(shadow, (rect.x + dx, rect.y + dy))
            self.screen.blit(text, rect)
            rect = text.get_rect(center=(x, y - 20))
            self.screen.blit(text, rect)

    def draw_selection(self):
        if self.selected_piece is None:
            return
        rect = pygame.Rect(self.selected_piece.col * self.TILE_SIZE, self.selected_piece.row * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
        for row, col in self.available_moves:
            x, y = self.board_to_iso(row, col)
            pygame.draw.circle(self.screen, self.COLORS["move"], (x, y), 8)

    def handle_click(self, pos):
        row, col = self.iso_to_board(pos[0], pos[1])
        if not self.game.board.inside(row, col):
            return
        piece = self.game.board.get(row, col)
        if self.selected_piece is None:
            if (piece is not None and piece.color == self.game.turn):
                self.selected_piece = piece
                self.available_moves = self.game.legal_moves(piece)
            return
        if (row, col) in self.available_moves:
            self.game.move_piece(self.selected_piece, row, col)
            self.game.next_turn()
        self.selected_piece = None
        self.available_moves = []
    
    def print_historique(self, game):
        for move in game.move_history:
            print(move)
    
    def draw_turn(self):
        font = pygame.font.SysFont(None, 36)
        if self.game.turn == Color.WHITE:
            text = "Tour : Blanc"
            color = (255, 255, 255)
        else:
            text = "Tour : Noir"
            color = (0, 0, 0)
        surface = font.render(text, True, color)
        self.screen.blit(surface, (10, 10))
    
    def draw_status(self):
        font = pygame.font.SysFont(None, 36)
        status = {
            GameState.RUNNING: "",
            GameState.CHECK: "ECHEC !",
            GameState.CHECKMATE: "ECHEC ET MAT",
            GameState.STALEMATE: "PAT"
        }
        text = status[self.game.state]
        if text:
            surface = font.render(text, True, (255, 0, 0))
            self.screen.blit(surface, (10, 50))

# main
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_game()
                    elif event.key == pygame.K_l:
                        self.load_game()
            self.screen.fill((0, 100, 255))
            self.draw_board()
            self.draw_selection()
            self.draw_pieces()
            self.draw_turn()
            self.draw_status()
            pygame.display.flip()
            self.clock.tick(60)
        self.print_historique(self.game)
        pygame.quit()


if __name__ == "__main__":
    manager = GameManager()
    manager.run()
    
