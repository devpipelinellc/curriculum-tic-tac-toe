import random
# check if game is won.
def check_win(board):
    possible_wins = [
        board[0:3],
        board[3:6],
        board[6:9],
        board[0:7:3],
        board[1:8:3],
        board[2:9:3],
        board[::4],
        board[2:7:2]
    ]
    for combination in possible_wins:
        if combination == ['X', 'X', 'X']:
            return True
        elif combination == ['O', 'O', 'O']:
            return True
def possible_moves(board):
    moves = []
    for i in range(len(board)):
        if board[i] == '':
            moves.append(i)
    return moves
def win_or_block(board, letter):

    temp_board = board[::]
    possibilities = possible_moves(board)
    opponent_letter = 'X' if letter == 'O' else 'O'

    for i in possibilities:
        temp_board[i] = letter
        if check_win(temp_board):
            return i
        else:
            temp_board[i] = opponent_letter

        if check_win(temp_board):
            return i
        else:
            temp_board[i] = ''
            
def hold_possible_wins(temp_board):
    possible_wins = [
        temp_board[0:3],
        temp_board[3:6],
        temp_board[6:9],
        temp_board[0:7:3],
        temp_board[1:8:3],
        temp_board[2:9:3],
        temp_board[::4],
        temp_board[2:7:2]
    ]
    return possible_wins


def forced_win_block(board, letter):
    ways_to_win = 0
    possibilities = possible_moves(board)
    opponent_letter = 'O' if letter == 'X' else 'O'
    temp_board = board[::]
    wins_computer = [
        [letter, letter, ''],
        [letter, '', letter],
        ['', letter, letter]
    ]
    wins_opponent = [
        [opponent_letter, opponent_letter, ''],
        [opponent_letter, '', opponent_letter],
        ['', opponent_letter, opponent_letter]
    ]

    for i in possibilities:
        temp_board[i] = opponent_letter
        for combo in hold_possible_wins(temp_board):
            if combo == wins_opponent[0] or combo == wins_opponent[1] or combo == wins_opponent[2]:
                ways_to_win += 1
            if ways_to_win == 2:
                return i
        ways_to_win = 0
        temp_board[i] = letter
        for combo in hold_possible_wins(temp_board):
            if combo == wins_computer[0] or combo == wins_computer[1] or combo == wins_computer[2]:
                ways_to_win += 1
            if ways_to_win == 2:
                return i
        ways_to_win = 0
        temp_board[i] = ''


def forsee_win(board, letter):
    possibilities = possible_moves(board)
    temp_board = board[::]
    move_num = board.count('X') + board.count('O') + 1
    starting_move = [0, 2, 6, 8]

    if move_num == 1:
        return random.choice(starting_move)

    if move_num == 2 and board[4] == '':
        return 4

    if move_num == 2:
        return random.choice(starting_move)

    for i in possibilities:
        temp_board[i] = letter
        if forced_win_block(temp_board, letter):
            return forced_win_block(temp_board, letter)
        temp_board[i] = ''


def leftover_move(board):
    moves = possible_moves(board)
    return random.choice(moves)


def get_move(board, letter):
    win_block = win_or_block(board, letter)
    if win_block or win_block == 0:

        return win_block
    forced = forced_win_block(board, letter)
    if forced or forced == 0:
        return forced

    forsee = forsee_win(board, letter)
    if forsee or forsee == 0:
        return forsee

    leftover = leftover_move(board)
    if leftover or leftover == 0:
        return leftover