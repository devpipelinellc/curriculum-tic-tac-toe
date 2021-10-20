import os

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

def load_player_files():
   players_list = os.listdir('./players')
   output_list = []
   for player in players_list:
      if player != 'util.py':
         # Strip the '.py' from the end of the file name
         output_list.append(player.split('.')[0])
   return output_list

def get_printable_name(filename):
   return filename.title().replace('_', ' ')

def printable_players(file_list):
   output = []
   for player in file_list:
      # Title case the player file name and replace '_' with a space ' '
      output.append(get_printable_name(player))
   return output
