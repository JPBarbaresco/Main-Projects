board = [[[' ' for _ in range(3)] for _ in range(3)] for _ in range(9)]

def print_board():
    for i in range(0,9,3):
        for j in range(3):
            print(f"{board[i][j][0]}|{board[i][j][1]}|{board[i][j][2]} | {board[i+1][j][0]}|{board[i+1][j][1]}|{board[i+1][j][2]} | {board[i+2][j][0]}|{board[i+2][j][1]}|{board[i+2][j][2]}")
        if i < 6:
            print("---------------------")
# print_board()
def check_winner_board(game_board):
    # check rows:
    if board[game_board][0][0] == board[game_board][0][1] == board[game_board][0][2] and board[game_board][0][0] != ' ':
        if board[game_board][0][0] == 'x':
            return 'x'
        else:
            return 'o'
    elif board[game_board][1][0] == board[game_board][1][1] == board[game_board][1][2] and board[game_board][1][0] != ' ':
        if board[game_board][1][0] == 'x':
            return 'x'
        else:
            return 'o'
    elif board[game_board][2][0] == board[game_board][2][1] == board[game_board][2][2] and board[game_board][2][0] != ' ':
        if board[game_board][2][0] == 'x':
            return 'x'
        else:
            return 'o'
    #check columns:
    elif board[game_board][0][0] == board[game_board][1][0] == board[game_board][2][0] and board[game_board][0][0] != ' ':
        if board[game_board][0][0] == 'x':
            return 'x'
        else:
            return 'o'
    elif board[game_board][0][1] == board[game_board][1][1] == board[game_board][2][1]  and board[game_board][0][1] != ' ':
        if board[game_board][0][1] == 'x':
            return 'x'
        else:
            return 'o'
    elif board[game_board][0][2] == board[game_board][1][2] == board[game_board][2][2] and board[game_board][0][2] != ' ':
        if board[game_board][0][2] == 'x':
            return 'x'
        else:
            return 'o'
    #check diagonals:
    elif board[game_board][0][0] == board[game_board][1][1] == board[game_board][2][2] and board[game_board][0][0] != ' ':
        if board[game_board][0][0] == 'x':
            return 'x'
        else:
            return 'o'
    elif board[game_board][0][2] == board[game_board][1][1] == board[game_board][2][0] and board[game_board][0][2] != ' ':
        if board[game_board][0][2] == 'x':
            return 'x'
        else:
            return 'o'
    else:
        return None

def check_winner():
    # check rows:
    if check_winner_board(0) == check_winner_board(1) == check_winner_board(2) and check_winner_board(0) != None:
        return check_winner_board(0)
    elif check_winner_board(3) == check_winner_board(4) == check_winner_board(5) and check_winner_board(3) != None:
        return check_winner_board(3)
    elif check_winner_board(6) == check_winner_board(7) == check_winner_board(8) and check_winner_board(6) != None:
        return check_winner_board(6)
    # check columns:
    elif check_winner_board(0) == check_winner_board(3) == check_winner_board(6) and check_winner_board(0) != None:
        return check_winner_board(0)
    elif check_winner_board(1) == check_winner_board(4) == check_winner_board(7) and check_winner_board(1) != None:
        return check_winner_board(1)
    elif check_winner_board(2) == check_winner_board(5) == check_winner_board(8) and check_winner_board(2) != None:
        return check_winner_board(2)
    # check diagonals:
    elif check_winner_board(0) == check_winner_board(4) == check_winner_board(8) and check_winner_board(0) != None:
        return check_winner_board(0)
    elif check_winner_board(2) == check_winner_board(4) == check_winner_board(6) and check_winner_board(2) != None:
        return check_winner_board(2)
    else:
        return None

turns = 0
current_game_board = -1

while check_winner() == None:
    print_board()
    if turns == 0:
        while current_game_board not in range(0,9):
            user = input("Player 1 (x), choose a game board: ")
            if len(user) != 1:
                print("Invalid input. Please choose a single game board (0-8).")
            else:
                if user.lower() == 'q':
                    current_game_board = 0
                elif user.lower() == 'w':
                    current_game_board = 1
                elif user.lower() == 'e':
                    current_game_board = 2
                elif user.lower() == 'a':
                    current_game_board = 3
                elif user.lower() == 's':
                    current_game_board = 4
                elif user.lower() == 'd':
                   current_game_board = 5
                elif user.lower() == 'z':
                    current_game_board = 6
                elif user.lower() == 'x':
                    current_game_board = 7
                elif user.lower() == 'c':
                    current_game_board = 8
                else:
                    print("Invalid input.")
    else:
        user = input()
        if len(user) != 1:
            print("invalid input")
        else:
            if user.lower() == 'q':
                if turns % 2 != 0:
                    board[current_game_board][0][0] = 'x'
                else:
                    board[current_game_board][0][0] = 'o'
                current_game_board = 0
            elif user.lower() == 'w':
                if turns % 2 != 0:
                    board[current_game_board][0][1] = 'x'
                else:
                    board[current_game_board][0][1] = 'o'
                current_game_board = 1
            elif user.lower() == 'e':
                if turns % 2 != 0:
                    board[current_game_board][0][2] = 'x'
                else:
                    board[current_game_board][0][2] = 'o'
                current_game_board = 2
            elif user.lower() == 'a':
                if turns % 2 != 0:
                    board[current_game_board][1][0] = 'x'
                else:
                    board[current_game_board][1][0] = 'o'
                current_game_board = 3
            elif user.lower() == 's':
                if turns % 2 != 0:
                    board[current_game_board][1][1] = 'x'
                else:
                    board[current_game_board][1][1] = 'o'
                current_game_board = 4
            elif user.lower() == 'd':
                if turns % 2 != 0:
                    board[current_game_board][1][2] = 'x'
                else:
                    board[current_game_board][1][2] = 'o'
                current_game_board = 5
            elif user.lower() == 'z':
                if turns % 2 != 0:
                    board[current_game_board][2][0] = 'x'
                else:
                    board[current_game_board][2][0] = 'o'
                current_game_board = 6
            elif user.lower() == 'x':
                if turns % 2 != 0:
                    board[current_game_board][2][1] = 'x'
                else:
                    board[current_game_board][2][1] = 'o'
                current_game_board = 7
            elif user.lower() == 'c':
                if turns % 2 != 0:
                    board[current_game_board][2][2] = 'x'
                else:
                    board[current_game_board][2][2] = 'o'
                current_game_board = 8
            else:
                print("Invalid input.")

    print(check_winner())
    print(board[current_game_board])
    print(check_winner_board(current_game_board))
    turns += 1