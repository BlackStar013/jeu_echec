from logique_jeu import *

def main():
    game = Game()
    print_board(game.board)
    while(not(game.end)):
        print(f'It is {game.player_turn} turn.')
        init_row = int(input("Chose a row from where you want to move a piece : "))
        init_col = int(input("Chose a column from where you want to move a piece : "))
        dest_row = int(input("Chose a row where you want to move this piece : "))
        dest_col = int(input("Chose a column where you want to move this piece : "))
        if(0 <= init_row < 8 and 0 <= init_col < 8 and 0 <= dest_row < 8 and 0 <= dest_col < 8):
            resolve_move(game, init_row, init_col, dest_row, dest_col)
            if(is_white_check_mate(game)):
                print("the partie end, BLACK PLAYER won !")
                game.end = True
            elif(is_black_check_mate(game)):
                print("the partie end, WHITE PLAYER won !")
                game.end = True
            elif(is_white_in_check(game)):
                print("caution, white is currently in check")
            elif(is_black_in_check(game)):
                print("caution, black is currently in chack")
            print_board(game.board)
        else:
            print("wrong move, try again")
    print_board(game.board)
main()