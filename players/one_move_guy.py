from logic import *

def get_move(board, letter):
   # STEP 1
   weights = [5, 1, 5, 1, 4, 1, 5, 1, 5]
   available_moves = get_available_moves(board)
   
   # STEP 2
   move_scores = [0] * 9
   for move_index in available_moves:
      move_scores[move_index] = get_score(board, letter, move_index)
   
   # STEP 3
   move_weighted_scores = []
   for i in range(9):
      move_weighted_scores.append(weights[i] * move_scores[i])
   
   # STEP 4
   return get_highest_index(move_weighted_scores)

def get_score(board, letter, move):
   temp_board = board[::]

   temp_board[move] = letter
   
   winner = get_winner(temp_board)

   if winner == '':
      return 1
   if winner == letter:
      return 50
   
   return -1

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

# print(get_move(['X','O','X','X','O','O','O','',''], 'X'))

#  3 | 1 | 3
# ---+---+---
#  1 | 5 | 1
# ---+---+---
#  3 | 1 | 3
# # STEP 1
# weights = [3, 1, 3, 1, 5, 1, 3, 1, 3]

#  0 | 1 | 1
# ---+---+---
#  0 | 0 | 1
# ---+---+---
#  1 | 1 | 0
# # STEP 2
# scores = [0, 1, 1, 0, 0, 1, 1, 1, 0]

#  0 | 1 | 3
# ---+---+---
#  0 | 0 | 1
# ---+---+---
#  3 | 1 | 0
# # STEP 3
# weighted_scores = [0, 1, 3, 0, 0, 1, 3, 1, 0]

# # STEP 4
# Pick the highest one, or one of the highest ones

