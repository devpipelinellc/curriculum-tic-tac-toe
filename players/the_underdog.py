from logic import *
import random

def get_move(board, letter):
   # STEP 1
   weights = [5, 1, 5, 1, 5, 1, 5, 1, 5]
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
   move = get_highest_index(move_weighted_scores)
   if not move or move not in available_moves:
      return random.choice(available_moves)
   return move

def get_score(board, letter, move, opponent = False):
   temp_board = board[::]

   # Place the hypothetical piece into the temporary board to see how it works :)
   temp_board[move] = letter
   
   winner = get_winner(temp_board)

   if winner == letter:
      # We have a winner, just return the 100 score
      return 100
   
   if opponent == True:
      return 1

   # Since this isn't a winner, let's see if it is a potential loser
   opp_letter = 'X' if letter == 'O' else 'O'
   available_moves = get_available_moves(temp_board)
   
   for move_index in available_moves:
      temp_score = get_score(temp_board, opp_letter, move_index, True)
      if temp_score >= 100:
         return -1
   
   return 1

def get_highest_index(list_of_numbers):
   if len(list_of_numbers) < 1:
      return None
   max_indexes = []
   max_n = -1
   for i, n in enumerate(list_of_numbers):
      if n > max_n:
         max_indexes = [i]
         max_n = n
      elif n == max_n:
         max_indexes.append(i)
   return random.choice(max_indexes)

def get_available_moves(board):
   output = []
   for i in range(len(board)):
      if board[i] == '':
         output.append(i)
   
   return output

# print(get_move(['O','X','O','','X','','O','',''], 'X'))

