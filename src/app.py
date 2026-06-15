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
)


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

    # pour tester déjà en 2D avant la partie isométrique
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if((row + col) % 2 == 0):
                    color = self.COLORS["light"]
                else:
                    color = self.COLORS["dark"]
                rect = pygame.Rect(col * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def piece_symbol(self, piece):
        symbols = {
            Pawn: "P",
            Tower: "T",
            Knight: "C",
            Bishop: "F",
            Queen: "Q",
            King: "K",
        }
        letter = symbols[type(piece)]
        if piece.color == Color.BLACK:
            return letter.lower()
        return letter

    def draw_pieces(self):
        font = pygame.font.SysFont(None, 50)
        for row in self.game.board.grid:
            for piece in row:
                if piece is None:
                    continue
                text = font.render(self.piece_symbol(piece), True, (0, 0, 0))
                x = piece.col * self.TILE_SIZE + 30
                y = piece.row * self.TILE_SIZE + 20
                self.screen.blit(text, (x, y))

    def draw_selection(self):
        if self.selected_piece is None:
            return
        rect = pygame.Rect(self.selected_piece.col * self.TILE_SIZE, self.selected_piece.row * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
        pygame.draw.rect(self.screen, self.COLORS["selected"], rect, 4)
        for row, col in self.available_moves:
            center = (col * self.TILE_SIZE + self.TILE_SIZE // 2, row * self.TILE_SIZE + self.TILE_SIZE // 2)
            pygame.draw.circle(self.screen, self.COLORS["move"], center, 10)

    def handle_click(self, pos):
        col = pos[0] // self.TILE_SIZE
        row = pos[1] // self.TILE_SIZE
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
            self.screen.fill((0, 0, 0))
            self.draw_board()
            self.draw_selection()
            self.draw_pieces()
            pygame.display.flip()
            self.clock.tick(60)
        self.print_historique(self.game)
        pygame.quit()


if __name__ == "__main__":
    manager = GameManager()
    manager.run()
    
