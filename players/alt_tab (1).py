winning_conditions = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [6,4,2],
]

double_win_traps = [[0, 1, 3], [0, 1, 6], [0, 2, 3], [0, 2, 6], [0, 1, 4], [0, 1, 7], [1, 2, 4], [1, 2, 7], [0, 2, 5], [0, 2, 8], [1, 2, 5], [1, 2, 8], [0, 1, 8], [0, 2, 4], [1, 2, 6], [0, 3, 4], [3, 4, 6], [0, 3, 5], [3, 5, 6], [1, 3, 4], [3, 4, 7], [1, 4, 5], [4, 5, 7], [2, 3, 5], [3, 5, 8], [2, 4, 5], [4, 5, 8], [3, 4, 8], [0, 4, 5], [2, 3, 4], [4, 5, 6], [0, 6, 7], [3, 6, 7], [0, 6, 8], [3, 6, 8], [1, 6, 7], [4, 6, 7], [1, 7, 8], [4, 7, 8], [2, 6, 8], [5, 6, 8], [2, 7, 8], [5, 7, 8], [4, 6, 8], [0, 7, 8], [2, 6, 7], [0, 3, 8], [0, 4, 6], [2, 3, 6], [1, 4, 8], [0, 4, 7], [1, 4, 6], [2, 4, 7], [2, 4, 8], [0, 5, 8], [2, 5, 6]]

corner_spaces = [0,2,6,8]
edge_spaces = [1,3,5,7]
center_space = [4]

def get_move(board, letter):
    opposite_letter = "X" if letter == "O" else "O"
    global corner_spaces
    global edge_spaces
    global center_space
    weights = [
        2,1,2,
        1,1.5,1,
        2,1,2
    ]
    #check for a move to win
    winning_move = check_board_for_win(board, letter)
    if not isinstance(winning_move, bool):
        # print("Winning Move")
        return winning_move

    #check for a move to block a win
    blocking_move = check_board_for_win(board, opposite_letter)
    if not isinstance(blocking_move, bool):
        # print("Blocking Move")
        return blocking_move

    #check for a double win trap
    trap_move = check_board_for_double_win_trap(board, letter)
    if not isinstance(trap_move, bool):
        # print("Setting up a Trap")
        return trap_move

    #check for a move to block a trap
    opponents_trap_move = check_board_for_double_win_trap(board, opposite_letter)
    if not isinstance(opponents_trap_move, bool):
        if check_board_for_moves(board, opposite_letter, [0,8]) and check_board_for_moves(board, letter, [4]) or check_board_for_moves(board, opposite_letter, [2,6]) and check_board_for_moves(board, letter, [4]):
            return 7
        if check_board_for_moves(board, opposite_letter, [5,6]) and check_board_for_moves(board, letter, [4]):
            return 8
        if check_board_for_moves(board, opposite_letter, [0,7]) and check_board_for_moves(board, letter, [4]):
            return 6
        if check_board_for_moves(board, opposite_letter, [1,8]) and check_board_for_moves(board, letter, [4]):
            return 2
        if check_board_for_moves(board, opposite_letter, [7]) and check_board_for_moves(board, opposite_letter, [0,2], 1):
            return 8
        if check_board_for_moves(board, opposite_letter, [5]) and check_board_for_moves(board, opposite_letter, [0,6], 1):
            return 2
        if check_board_for_moves(board, opposite_letter, [1]) and check_board_for_moves(board, opposite_letter, [6,8], 1):
            return 0
        if check_board_for_moves(board, opposite_letter, [3]) and check_board_for_moves(board, opposite_letter, [2,8], 1):
            return 6

    #get the number of moves made and then play accordingly
    num_moves_made = get_num_moves_made(board)
    if num_moves_made == 0: return 0
    if num_moves_made == 1:
        #if the one move is in the corner
        if check_board_for_moves(board, opposite_letter, corner_spaces, 1): return 4

        #if the one move is on the edge
        if check_board_for_moves(board, opposite_letter, edge_spaces, 1): return 4

        #if the one move is in the center
        else: return 0
    if num_moves_made == 2:
        if check_board_for_moves(board, opposite_letter, [1]):
            return 6
        if check_board_for_moves(board, opposite_letter, [2]):
            return 6
        if check_board_for_moves(board, opposite_letter, [3]):
            return 2
        if check_board_for_moves(board, opposite_letter, [4]):
            return 8
        if check_board_for_moves(board, opposite_letter, [5]):
            return 4
        if check_board_for_moves(board, opposite_letter, [6]):
            return 2
        if check_board_for_moves(board, opposite_letter, [7]):
            return 4
        if check_board_for_moves(board, opposite_letter, [8]):
            return 6
    # if num_moves_made == 3:
    #     if check_board_for_moves(board, opposite_letter, [0,8]) and check_board_for_moves(board, letter, [4])
    possible_moves = get_weighted_moves(board, weights)
    if max(possible_moves) > 0:
        return possible_moves.index(max(possible_moves))
    return

def get_num_moves_made(board):
    num_moves = 0
    for i in range(len(board)):
        if board[i] != '':
            num_moves += 1
    return num_moves

def check_board_for_moves(board, letter, positions, num_to_match = -1):
    if num_to_match == -1: num_to_match = len(positions) #if num_to_match is -1, require all to match
    num = 0
    for pos in positions:
        if board[pos] == letter:
            num += 1
        if num >= num_to_match:
            return True
    return False

def get_weighted_moves(board, weights):
    weighted_moves = []
    for i in range(len(board)):
        if board[i] == "":
            weighted_moves.append(weights[i])
        else:
            weighted_moves.append(0)
    return weighted_moves

def check_board_for_win(board, letter):
    for position in range(len(board)):
        temp_board = board[::]
        if temp_board[position] == '':
            temp_board[position] = letter
            if (check_for_win(temp_board)):
                return position
    return False

def check_for_win(board):
    global winning_conditions
    for win_condition in winning_conditions:
        if (board[win_condition[0]] == board[win_condition[1]] == board[win_condition[2]] != ''):
            return True
    return False

def check_board_for_double_win_trap(board, letter):
    for position in range(len(board)):
        temp_board = board[::]
        if temp_board[position] == '':
            temp_board[position] = letter
            if check_for_double_win_trap(temp_board, letter):
                return position
    return False

def check_for_double_win_trap(board, letter):
    global double_win_traps
    opposite_letter = "X" if letter == "O" else "O"
    for trap in double_win_traps:
        if board[trap[0]] == board[trap[1]] == board[trap[2]] == letter != '':
            opponents_block = check_board_for_win(board, letter)
            if not isinstance(opponents_block, bool):
                temp_board = board[::]
                temp_board[opponents_block] = opposite_letter
                successful_trap = check_board_for_win(temp_board, letter)
                if not isinstance(successful_trap, bool):
                    return True
    return False

def get_double_win_traps():
    global winning_conditions
    double_win_traps = []
    for win_condition in winning_conditions:
        for win_check in winning_conditions:
            for pos in win_condition:
                if pos in win_check and win_condition != win_check:
                    list1 = win_condition[::]
                    list2 = win_check[::]
                    list1.remove(pos)
                    list2.remove(pos)
                    for i in list1:
                        for j in list2:
                            double_win_trap = [pos,i,j]
                            double_win_trap.sort()
                            if double_win_trap not in double_win_traps:
                                double_win_traps.append(double_win_trap)
    return double_win_traps

def print_board(board):
    printable_board = board[::]
    for i in range(len(printable_board)):
        if printable_board[i] == "": printable_board[i] = " "
            
    print(f"┌───┬───┬───┐\n│ {printable_board[0]} │ {printable_board[1]} │ {printable_board[2]} │\n├───┼───┼───┤\n│ {printable_board[3]} │ {printable_board[4]} │ {printable_board[5]} │\n├───┼───┼───┤\n│ {printable_board[6]} │ {printable_board[7]} │ {printable_board[8]} │\n└───┴───┴───┘")

def main():
    board = [
        '','','',
        '','','',
        '','',''
    ]
    letter = "X"
    playing = ""
    while playing != "q":
        next_move = get_move(board, letter)
        if next_move != None:
            board[next_move] = letter
            print_board(board)
            letter = "X" if letter == "O" else "O"
            playing = input("")
        else: playing = "q"
        if check_for_win(board): playing = "q"
    #print(get_move(board,"X"))

# main()
# print(get_double_win_traps())