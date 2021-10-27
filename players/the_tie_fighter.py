import random

def get_move(board, letter):
   opponent_letter = 'X' if letter == 'O' else 'O'
   available_moves = get_available_moves(board)
   turn_number = 10-len(available_moves)
   weights = [1] * 9
   corners = [0,2,6,8]
   sides = [1,3,5,7]
   opposite_indexes = [8, 7, 6, 5, -1, 3, 2, 1, 0] 

   if turn_number == 1: return 0
   elif turn_number == 2:
      if find_move(board, sides, opponent_letter) >= 0:
         return 4
      
      weights = [5, 0, 5, 0, 10, 0, 5, 0, 5]
      for m in list(range(1,8))[::2]: # [1, 3, 5, 7]
         if board[m] != '': 
            weights = [10, 0, 10, 0, 0, 0, 10, 0, 10]
   elif turn_number == 3: 
      if find_move(board, [8], opponent_letter) >= 0:
         return 4
      weights = [10, 0, 0, 0, 0, 0, 0, 0, 10]
   elif turn_number == 4:
      weights = [0, 10, 0, 10, 0, 10, 0, 10, 0]
      # If the opponent has moved both sides, select a corner next to one of the sides
      side_play = find_move(board, sides, opponent_letter)
      if side_play > 0 and find_move(board, corners, opponent_letter) < 0:
         total_weights = [
            [10,0,10,0,0,0,0,0,0],
            [10,0,0,0,0,0,10,0,0],
            [0,0,10,0,0,0,0,0,10],
            [0,0,0,0,0,0,10,0,10],
         ]
         weights = total_weights[(side_play - 1) // 2]
         
      # Not all sides are created equal in this case
      blocks = [[1,7], [3,5]]
      for m in list(range(1,8))[::2]:
         opp_space_value = board[opposite_indexes[m]]
         if opp_space_value == opponent_letter:
            weights[m] = 4

      # Do we need to favor corners
      bad_conditions = [[0, 4, 8], [2, 4, 6]]
      for c in bad_conditions:
         if (board[c[0]] != '' and board[c[1]] != '' and board[c[2]] != '') and board[c[0]] != board[c[2]]:
            weights = [10, 0, 10, 0, 0, 0, 10, 0, 10]
            break
      
      # Check the loss condition from a single corner and a side played by the opponent
      opp_corner_move = find_move(board, corners, opponent_letter)
      opp_side_move = find_move(board, sides, opponent_letter)
      if opp_corner_move >= 0 and opp_side_move >= 0:
         # Block if there is a need to block
         for move_index in available_moves:
            temp_board = board[::]
            temp_score = get_score(temp_board, opponent_letter, move_index, True)
            if temp_score >= 100:
               return move_index
         # Favor the corner opposite the corner the opponent moved into
         if opposite_indexes[opp_corner_move] in available_moves:
            return opposite_indexes[opp_corner_move]

   # Look for wins or blocks
   for temp_letter in [letter, opponent_letter]:
      for move_index in available_moves:
         temp_board = board[::]
         temp_score = get_score(temp_board, temp_letter, move_index, True)
         if temp_score >= 100:
            return move_index
   
   move_scores = [-2] * 9
   for move_index in available_moves:
      move_scores[move_index] = get_score(board, letter, move_index)
   
   move_weighted_scores = []
   for i in range(9):
      move_weighted_scores.append(weights[i] * move_scores[i])
   
   if len(move_weighted_scores) > 0:
      move = get_highest_index(move_weighted_scores)
   if move is None or move not in available_moves:
      return random.choice(available_moves)
   return move

def find_move(board, indexes, opponent_letter):
   for m in indexes:
      if board[m] == opponent_letter:
         return m
   return -1

def get_score(board, letter, move, opponent = False):
   temp_board = board[::]

   # Place the hypothetical piece into the temporary board to see how it works :)
   temp_board[move] = letter
   winner = get_winner(temp_board)
   if winner == letter:
      return 100
   
   if opponent == True:
      return 1

   # Since this isn't a winner, let's see if it is a potential loser
   opp_letter = 'X' if letter == 'O' else 'O'
   available_moves = get_available_moves(temp_board)
   
   for move_index in available_moves:
      if get_score(temp_board, opp_letter, move_index, True) >= 100:
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

def get_available_moves(board):
   output = []
   for i in range(len(board)):
      if board[i] == '':
         output.append(i)
   
   return output
