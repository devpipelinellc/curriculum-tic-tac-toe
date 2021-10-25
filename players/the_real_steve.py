
board = ['','',''
        ,'X','O','',
         '','X','']

def get_winner(board):
   checks = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6]
   ]
   for indexes in checks:
      if board[indexes[0]] == board[indexes[1]] == board[indexes[2]] != '':
         return board[indexes[0]]
   
   return ''
   
def get_score(board, letter, move):
    temp_board = board[::]  
    
    temp_board[move] = letter

    winner = get_winner(temp_board)

    if winner == letter:
       temp_board = board[::]
       return 50
    if winner == '':
        return 1
    return -1
    
def block(board, letter, move):
    temp_board = board[::]
    
    if letter.upper() == 'X':
        opponents_mark = 'O'
    elif letter.upper() == 'O':
        opponents_mark = 'X'    
    
    temp_board[move] = opponents_mark
    winner = get_winner(temp_board)

    if winner == opponents_mark:
        return 25
    else:
        return 1
    
def get_highest_index(list_of_numbers):
    max_index = -1
    max_n = -1
    for i, n in enumerate(list_of_numbers):
        if n > max_n:
            max_index = i
            max_n = n

    return max_index

def get_available_moves(board):
    output = []
    for i in range(len(board)):
        if board[i] == '':
            output.append(i)

    return output

def get_move(board, letter):
    if letter.upper() == 'X':
        opponents_mark = 'O'
    elif letter.upper() == 'O':
        opponents_mark = 'X'
    
    if board[4] == letter.upper():    
        
        if board == ['', letter, '', opponents_mark, letter, '', '', opponents_mark, ''] or board == ['', letter, '', '' , letter, opponents_mark, '', opponents_mark, '']:
            weights = [2, 1, 2, 1, 3, 1, 6, 1, 6]
        elif letter.upper() == 'O' and (board == ['', '', '', 'X', 'O', '', '', 'X', ''] or board == ['', '', '', '' , 'O', 'X', '', 'X', '']):
            weights = [2, 1, 2, 1, 3, 1, 6, 1, 6]
        else:
            weights = [1, 2, 1, 2, 3, 2, 1, 2, 1]

    else:
        weights = [2, 1, 2, 1, 3, 1, 2, 1, 2]
    available_moves = get_available_moves(board)

    move_scores = [0] * 9
    for move_index in available_moves:
        move_scores[move_index] = get_score(board, letter, move_index)

    block_scores = [0] *9
    for move_index in available_moves:
        block_scores[move_index] = block(board, letter, move_index)
    
    move_weighted_scores = []
    for i in range(9):
        move_weighted_scores.append(weights[i] * move_scores[i] * block_scores[i])
    # print(move_weighted_scores)
    return get_highest_index(move_weighted_scores)
