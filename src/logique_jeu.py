# MOVEMENT FOR A PION
def movement_pion(game, x_init, y_init, x_dest, y_dest):
    pion = game.board[x_init][y_init]
    if pion == 0:  # empty case
        return False
    if game.player_turn != pion.color:
        return False
    direction = -1 if pion.color == 0 else 1
    start_row = 6 if pion.color == 0 else 1
    enemy_color = 1 if pion.color == 0 else 0
    #  1 case
    if x_dest == x_init + direction and y_dest == y_init:
        if game.board[x_dest][y_dest] == 0:
            return True
    # 2 cases (first move)
    if x_init == start_row and x_dest == x_init + 2 * direction and y_dest == y_init:
        if (game.board[x_init + direction][y_init] == 0 and
            game.board[x_dest][y_dest] == 0):
            return True
    # eat in diagonal
    if x_dest == x_init + direction and abs(y_dest - y_init) == 1:
        target = game.board[x_dest][y_dest]
        if target != 0 and target.color == enemy_color:
            return True
    return False


# MOVEMENT FOR A TOWER
def movement_tower(game, x_init, y_init, x_dest, y_dest):
    pion = game.board[x_init][y_init]
    if pion == 0:
        return False
    if game.player_turn != pion.color:
        return False
    # ligne
    if x_init == x_dest:
        step = 1 if y_dest > y_init else -1
        for y in range(y_init + step, y_dest, step):
            if game.board[x_init][y] != 0:
                return False
    # colonne
    elif y_init == y_dest:
        step = 1 if x_dest > x_init else -1
        for x in range(x_init + step, x_dest, step):
            if game.board[x][y_init] != 0:
                return False
    else:
        return False
    target = game.board[x_dest][y_dest]
    return target == 0 or target.color != game.player_turn


# MOVEMENT FOR A FOUL
def movement_foul(game, x_init, y_init, x_dest, y_dest):
    pion = game.board[x_init][y_init]
    if pion == 0:
        return False
    if game.player_turn != pion.color:
        return False
    if abs(x_dest - x_init) != abs(y_dest - y_init):
        return False
    signe_x = 1 if x_dest > x_init else -1
    signe_y = 1 if y_dest > y_init else -1
    for i in range(1, abs(x_dest - x_init)):
        x = x_init + i * signe_x
        y = y_init + i * signe_y
        if game.board[x][y] != 0:
            return False
    target = game.board[x_dest][y_dest]
    return target == 0 or target.color != game.player_turn


# MOVEMENT FOR A HORSE
def movement_horse(game, x_init, y_init, x_dest, y_dest):
    pion = game.board[x_init][y_init]
    if pion == 0: 
        return False
    if(game.player_turn != pion.color):
        print("it is not your piece")
        return False
    # if the dest case is empty or occupied by the other player, and it matches the move of the horse piece
    if(((game.board[x_dest][y_dest] == 0) or (game.board[x_dest][y_dest] != 0 and game.board[x_dest][y_dest].color != game.player_turn)) and (
        ((x_dest == x_init+2 and y_dest == y_init+1) or
        (x_dest == x_init+2 and y_dest == y_init-1) or
        (x_dest == x_init+1 and y_dest == y_init+2) or
        (x_dest == x_init-1 and y_dest == y_init+2) or
        (x_dest == x_init-2 and y_dest == y_init+1) or
        (x_dest == x_init-2 and y_dest == y_init-1) or
        (x_dest == x_init+1 and y_dest == y_init-2) or
        (x_dest == x_init-1 and y_dest == y_init-2)))):
        return True
    return False


# MOVEMENT FOR A QUEEN
def movement_queen(game, x_init, y_init, x_dest, y_dest):
    pion = game.board[x_init][y_init]
    if pion == 0:
        return False
    if(game.player_turn != pion.color):
        print("it is not your piece")
        return False
    if((movement_tower(game, x_init, y_init, x_dest, y_dest) or movement_foul(game, x_init, y_init, x_dest, y_dest))):
        return True
    return False


def is_white_in_check(game):
    old_turn = game.player_turn
    game.player_turn = 1  # simulate black
    king = game.list_pieces[0][0]
    for piece in game.list_pieces[1]:
        if piece.movement(game, piece.x, piece.y, king.x, king.y):
            game.player_turn = old_turn
            return True
    game.player_turn = old_turn
    return False

def is_black_in_check(game):
    old_turn = game.player_turn
    game.player_turn = 0  # simulate white
    king = game.list_pieces[1][0]
    for piece in game.list_pieces[0]:
        if piece.movement(game, piece.x, piece.y, king.x, king.y):
            game.player_turn = old_turn
            return True
    game.player_turn = old_turn
    return False


# MOVEMENT FOR A KING
def movement_king(game, x_init, y_init, x_dest, y_dest):
    pion = game.board[x_init][y_init]
    if pion == 0:
        return False
    if game.player_turn != pion.color:
        return False
    if abs(x_dest - x_init) <= 1 and abs(y_dest - y_init) <= 1:
        target = game.board[x_dest][y_dest]
        if target == 0 or target.color != game.player_turn:
            # SIMULATION
            game.board[x_init][y_init] = 0
            game.board[x_dest][y_dest] = pion
            old_x, old_y = pion.x, pion.y
            pion.x, pion.y = x_dest, y_dest
            if game.player_turn == 0:
                check = is_white_in_check(game)
            else:
                check = is_black_in_check(game)
            # UNDO
            game.board[x_init][y_init] = pion
            game.board[x_dest][y_dest] = target
            pion.x, pion.y = old_x, old_y
            return not check
    return False


class Pions:
    def __init__(self, id, x, y, starting_case, color, movement, has_mooved):
        '''id = +/- [1-6]; starting_case = (x,y); color = 1 for black and 0 for white; movement = function of movement of the pion'''
        self.id = id
        self.x = x
        self.y = y
        self.starting_case = starting_case
        self.color = color
        self.movement = movement
        self.has_mooved = has_mooved
# Init Pions BLACK PLAYER
b_t_l = Pions(-4, 0, 0, (0,0), 1, movement_tower, False) # b->black; t->tower; l->left
b_h_l = Pions(-2, 0, 1, (0,1), 1, movement_horse, False) # black horse left
b_f_l = Pions(-3, 0, 2, (0,2), 1, movement_foul, False) # black foul left
b_q = Pions(-5, 0, 3, (0,3), 1, movement_queen, False) # black queen
b_k = Pions(-6, 0, 4, (0,4), 1, movement_king, False) # black king
b_f_r = Pions(-3, 0, 5, (0,5), 1, movement_foul, False) # black foul right
b_h_r = Pions(-2, 0, 6, (0,6), 1, movement_horse, False) # black horse right
b_t_r = Pions(-4, 0, 7, (0,7), 1, movement_tower, False) # black tower right
b_p1 = Pions(-1, 1, 0, (1,0), 1, movement_pion, False) # black pion 1
b_p2 = Pions(-1, 1, 1, (1,1), 1, movement_pion, False) # black pion 2
b_p3 = Pions(-1, 1, 2, (1,2), 1, movement_pion, False) # black pion 3
b_p4 = Pions(-1, 1, 3, (1,3), 1, movement_pion, False) # black pion 4
b_p5 = Pions(-1, 1, 4, (1,4), 1, movement_pion, False) # black pion 5
b_p6 = Pions(-1, 1, 5, (1,5), 1, movement_pion, False) # black pion 6
b_p7 = Pions(-1, 1, 6, (1,6), 1, movement_pion, False) # black pion 7
b_p8 = Pions(-1, 1, 7, (1,7), 1, movement_pion, False) # black pion 8
# Init Pions WHITE PLAYER
w_t_l = Pions(4, 6, 0, (6,0), 0, movement_tower, False) # w->white; t->tower; l->left
w_h_l = Pions(2, 6, 1, (6,1), 0, movement_horse, False) # white horse left
w_f_l = Pions(3, 6, 2, (6,2), 0, movement_foul, False) # white foul left
w_q = Pions(5, 6, 3, (6,3), 0, movement_queen, False) # white queen
w_k = Pions(6, 6, 4, (6,4), 0, movement_king, False) # white king
w_f_r = Pions(3, 6, 5, (6,5), 0, movement_foul, False) # white foul right
w_h_r = Pions(2, 6, 6, (6,6), 0, movement_horse, False) # white horse right
w_t_r = Pions(4, 6, 7, (6,7), 0, movement_tower, False) # white tower right
w_p1 = Pions(1, 7, 0, (7,0), 0, movement_pion, False) # white pion 1
w_p2 = Pions(1, 7, 1, (7,1), 0, movement_pion, False) # white pion 2
w_p3 = Pions(1, 7, 2, (7,2), 0, movement_pion, False) # white pion 3
w_p4 = Pions(1, 7, 3, (7,3), 0, movement_pion, False) # white pion 4
w_p5 = Pions(1, 7, 4, (7,4), 0, movement_pion, False) # white pion 5
w_p6 = Pions(1, 7, 5, (7,5), 0, movement_pion, False) # white pion 6
w_p7 = Pions(1, 7, 6, (7,6), 0, movement_pion, False) # white pion 7
w_p8 = Pions(1, 7, 7, (7,7), 0, movement_pion, False) # white pion 8


class Game:
    def __init__(self):
        self.board = self.init_board()
        self.player_turn = 0
        self.end = False
        # to verifie the check condition, and the kings are in first place to access them easily
        self.list_pieces = [[w_k, w_p1, w_p2, w_p3, w_p4, w_p5, w_p6, w_p7, w_p8, w_t_l, w_h_l, w_f_l, w_q, w_f_r, w_h_r, w_t_r],
                            [b_k, b_t_l, b_h_l, b_f_l, b_q, b_f_r, b_h_r, b_t_r, b_p1, b_p2, b_p3, b_p4, b_p5, b_p6, b_p7, b_p8]]
        
    def init_board(self):
        return [[b_t_l, b_h_l, b_f_l, b_q, b_k, b_f_r, b_h_r, b_t_r],
                [b_p1, b_p2, b_p3, b_p4, b_p5, b_p6, b_p7, b_p8],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [w_p1, w_p2, w_p3, w_p4, w_p5, w_p6, w_p7, w_p8],
                [w_t_l, w_h_l, w_f_l, w_q, w_k, w_f_r, w_h_r, w_t_r]]
dico = {
    -1:("1", "\033[31m"), -2:("2", "\033[31m"), -3:("3", "\033[31m"),
    -4:("4", "\033[31m"), -5:("5", "\033[31m"), -6:("6", "\033[31m"),
    0:(" ", ""),
    1:("1", "\033[34m"), 2:("2", "\033[34m"), 3:("3", "\033[34m"),
    4:("4", "\033[34m"), 5:("5", "\033[34m"), 6:("6", "\033[34m")
}

def get_square(i, j):
    if (i + j) % 2 == 0:
        return "\033[47m"  # blanc
    else:
        return "\033[40m" # noir


def print_board(board):
    print("♟->1, ♞->2, ♝->3, ♜->4, ♛->5, ♚->6")
    print("     0  1  2  3  4  5  6  7")
    for i in range(8):
        row = f" {i}  "
        for j in range(8):
            square = get_square(i, j)
            if(board[i][j] != 0):
                char, color = dico[board[i][j].id]
            else:
                char, color = dico[board[i][j]]

            # largeur fixe (3 espaces)
            content = f"{char:^3}"

            row += f"{square}{color}{content}\033[0m"
        print(row + f"  {i}")
    print("     0  1  2  3  4  5  6  7\n")


def remove_piece(game, piece):
    enemy_list = game.list_pieces[(game.player_turn + 1) % 2]
    if piece in enemy_list:
        enemy_list.remove(piece)

def resolve_move(game, x_init, y_init, x_dest, y_dest):
    piece = game.board[x_init][y_init]
    if piece == 0:
        print("No piece here")
        return False
    if not piece.movement(game, x_init, y_init, x_dest, y_dest):
        print("Invalid move")
        return False
    target = game.board[x_dest][y_dest]
    old_x, old_y = piece.x, piece.y
    game.board[x_init][y_init] = 0
    game.board[x_dest][y_dest] = piece
    piece.x, piece.y = x_dest, y_dest
    illegal = is_white_in_check(game) if game.player_turn == 0 else is_black_in_check(game)
    if illegal:
        game.board[x_init][y_init] = piece
        game.board[x_dest][y_dest] = target
        piece.x, piece.y = old_x, old_y
        print("Move puts your king in check")
        return False
    if target != 0:
        remove_piece(game, target)
    piece.has_mooved = True
    if piece.id in [1, -1]: # if it is a pion
        if (piece.color == 0 and x_dest == 0) or (piece.color == 1 and x_dest == 7):
            while True:
                choice = input("Promote to (q = queen, t = tower, f = foul, h = horse): ").lower()
                if choice in ["q", "t", "f", "h"]:
                    break
            if choice == "t":
                piece.id = 4 if piece.color == 0 else -4
                piece.movement = movement_tower
            elif choice == "f":
                piece.id = 3 if piece.color == 0 else -3
                piece.movement = movement_foul
            elif choice == "h":
                piece.id = 2 if piece.color == 0 else -2
                piece.movement = movement_horse
            else:
                piece.id = 5 if piece.color == 0 else -5
                piece.movement = movement_queen
    game.player_turn = (game.player_turn + 1) % 2
    return True


def has_any_legal_move(game, color):
    old_turn = game.player_turn
    game.player_turn = color
    for piece in game.list_pieces[color]:
        for x in range(8):
            for y in range(8):
                if piece.movement(game, piece.x, piece.y, x, y):
                    target = game.board[x][y]
                    old_x, old_y = piece.x, piece.y
                    game.board[old_x][old_y] = 0
                    game.board[x][y] = piece
                    piece.x, piece.y = x, y
                    if color == 0:
                        check = is_white_in_check(game)
                    else:
                        check = is_black_in_check(game)
                    # undo
                    game.board[old_x][old_y] = piece
                    game.board[x][y] = target
                    piece.x, piece.y = old_x, old_y

                    if not check:
                        game.player_turn = old_turn
                        return True
    game.player_turn = old_turn
    return False


def is_white_check_mate(game):
    return is_white_in_check(game) and not has_any_legal_move(game, 0)


def is_black_check_mate(game):
    return is_black_in_check(game) and not has_any_legal_move(game, 1)
