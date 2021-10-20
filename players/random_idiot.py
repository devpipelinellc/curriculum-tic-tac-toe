import random

def get_move(board, letter):
   available_moves = get_available_moves(board)
   
   return random.choice(available_moves)

def get_available_moves(board):
   output = []
   for i in range(len(board)):
      if board[i] == '':
         output.append(i)
   
   return output