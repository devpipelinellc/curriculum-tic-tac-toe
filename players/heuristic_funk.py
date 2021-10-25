import random

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

def get_move(board, letter):
  corners = [0, 2, 6, 8]
  weights = [3, 1, 3, 1, 2, 1, 3, 1, 3]
  available_moves = get_available_moves(board)

  blist= []
  for i in available_moves:
    if i in corners:
      blist.append(i)

  if len(blist) == 4:
    random_corner = random.choice(blist)
    weights[random_corner] = 24
    
  if len(blist) < 4 and board[4] == '':
    weights[4] = 500

  move_scores = [0] * 9
  for move_index in available_moves:
    move_scores[move_index] = get_score(board, letter, move_index)

  move_weighted_scores = []
  for i in range(9):
    move_weighted_scores.append(weights[i] * move_scores[i])
  
  return get_highest_index(move_weighted_scores)

def get_score(board, letter, move, second_move=False):
  temp_board = board[::]
  temp_board[move] = letter
  winner = get_winner(temp_board)

  if winner == letter:
    return 100

  if second_move:
    return 1
  
  opp_letter = 'X' if letter == 'O' else 'O'

  if get_score(board, opp_letter, move, True) == 100:
    return 25

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