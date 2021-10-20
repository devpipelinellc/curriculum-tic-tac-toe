import importlib
import curses
from getch import getch
from logic import *
from time import sleep

symbols = ['X', 'O']

board_offset_y = 1
board_offset_x = 1

header = [
   "╔═════════════════════════════════════╗",
   "║        Tic-Tac-Toe Throwdown        ║",
   "╚═════════════════════════════════════╝"
]

main_board_display = [
   "                              ┌───────┐",
   "X :                           │ Moves │",
   "O :                           │ X │ O │",
   "                              ├───┼───┤",
   "        │   │                 │   │   │",
   "     ───┼───┼───              │   │   │",
   "        │   │                 │   │   │",
   "     ───┼───┼───              │   │   │",
   "        │   │                 │   │   │",
   "                              └───┴───┘"
]

many_games_results = [
   "┌───────────────────┬───────┬───────┬───────┐",
   "│ Player Name       │ Win X │ Win O │ Total │",
   "├───────────────────┼───────┼───────┼───────┤",
   "│                   │       │       │       │",
   "├───────────────────┼───────┼───────┼───────┤",
   "│                   │       │       │       │",
   "└───────────────────┴───────┴───────┴───────┘"
]

global_stdscr = None
game_state = {
   'board' : [''] * 9,
   'moves_list' : [
      [],
      []
   ]
}

def draw_many_game_results():
   clear_board()
   draw_header()
   draw_template(board_offset_y + 4, board_offset_x, many_games_results)

def clear_board():
   global global_stdscr
   global_stdscr.clear()
   global_stdscr.refresh()

def draw_template(row, col, template_rows):
   global global_stdscr
   for line in template_rows:
      global_stdscr.addstr(row, col, line)
      row += 1
   global_stdscr.refresh()

def draw_header():
   draw_template(board_offset_y, board_offset_x, header)

def draw_menu(options):
   global global_stdscr
   global_stdscr.erase()
   draw_header()
   row = board_offset_y + 4
   col = board_offset_x + 3
   draw_template(row, col, options)
   global_stdscr.refresh()

def draw_main_menu():
   clear_board()
   options = [
      "(1) 1 Player",
      "(2) 2 Players (Custom AI's)",
      "(Q) Quit"
   ]
   draw_menu(options)

def draw_letter_select_menu():
   options = [
      "Which would you like to play?",
      "(X) : goes First",
      "(O)"
   ]
   draw_menu(options)

def draw_num_games_menu():
   options = [
      "(1) 1 Game",
      "(2) 10,000 Games"
   ]
   draw_menu(options)

def draw_ai_selection(player_files, letter='X'):
   
   players = printable_players(player_files)
   options = [f"Select an A.I. to play '{letter}'?"]

   for i, name in enumerate(players):
      options.append(f'({i}) {name}')
   
   draw_menu(options)

def get_ai_selection(player_files, letter='X'):
   draw_ai_selection(player_files, letter)
   
   index = 'not set'
   while ((not index.isnumeric()) or (int(index) < 0 or int(index) > len(player_files))):
      index = getch(list(map(str, list(range(len(player_files))))))
   
   return player_files[int(index)]

def draw_moves_list():
   global global_stdscr
   row = board_offset_y + 7
   col = board_offset_x + 32
   moves_list = game_state['moves_list']
   if len(moves_list[0]) == 0:
      return
   
   for player_idx in range(2):
      row = board_offset_y + 7
      for move in moves_list[player_idx]:
         global_stdscr.addstr(row, col + (player_idx * 4), str(move))
         row += 1
      
   global_stdscr.refresh()

def draw_board_display():
   global global_stdscr
   row = board_offset_y + 7
   col = board_offset_x + 6
   
   for i_row in range(3):
      for i_col in range(3):
         letter = game_state['board'][i_col + (i_row * 3)]
         # global_stdscr.addstr(row, col + (40), 'board:' + str(game_state['board']))
         if letter == '':
            global_stdscr.addstr(row + (2 * i_row), col + (i_col * 4), str(i_col + (i_row * 3)), curses.color_pair(1))
         else:
            global_stdscr.addstr(row + (2 * i_row), col + (i_col * 4), letter)
   
   global_stdscr.refresh()

def draw_main_board(players):
   global global_stdscr
   clear_board()
   row = board_offset_y
   col = board_offset_x
   draw_header()
   draw_template(row + 3, col, main_board_display)
   
   draw_moves_list()
   draw_board_display()
   draw_player_names(players)

   global_stdscr.refresh()

def print_message(message, row_offset = 0):
   global global_stdscr
   row = board_offset_y + 14 + row_offset
   col = board_offset_x

   global_stdscr.move(row, col)
   global_stdscr.deleteln()
   global_stdscr.addstr(row, col, message)

   global_stdscr.refresh()
   
def draw_player_names(players):
   global global_stdscr
   row = board_offset_y + 4
   col = board_offset_x + 4
   
   player_names = printable_players(players)
   for i, name in enumerate(player_names):
      global_stdscr.addstr(row + i, col, name)

   global_stdscr.refresh()

def print_many_games_scores(players, wins, wins2):
   global global_stdscr
   player_names = printable_players(players)

   row = board_offset_y + 7
   col = board_offset_x + 2
   
   global_stdscr.addstr(row, col, player_names[0])
   global_stdscr.addstr(row + 2, col, player_names[1])

   col += 21
   global_stdscr.addstr(row, col, str(wins[0]))
   global_stdscr.addstr(row + 2, col, str(wins[1]))

   col += 8
   global_stdscr.addstr(row, col, str(wins2[1]))
   global_stdscr.addstr(row + 2, col, str(wins2[0]))

   col += 8
   global_stdscr.addstr(row, col, str(wins[0] + wins2[1]))
   global_stdscr.addstr(row + 2, col, str(wins[1] + wins2[0]))


def play_game(players, print_board_during_play=True):
   global global_stdscr
   row = board_offset_y
   col = board_offset_x
   
   if len(players) < 2:
      raise Exception("Two players required to play the game!")

   # Initialize the board 
   game_state['board'] = [''] * 9
   valid_moves = list(range(9))
   game_state['moves_list'] = [[],[]]
   player_modules = []
   winner = ''
   turn = 1

   # Load the AI modules, when necessary
   if players[0] != 'Human':
      module_name = importlib.import_module('players.' + players[0])
      player_modules.append(module_name)
   else:
      player_modules.append(None)
   if players[1] != 'Human':
      module_name = importlib.import_module('players.' + players[1])
      player_modules.append(module_name)
   else:
      player_modules.append(None)
   
   # Begin game loop 
   while winner == '' and len(valid_moves) > 0:
      if print_board_during_play:
         draw_main_board(players)

      turn = (turn + 1) % 2
      if players[turn] == 'Human':
         # If player turn is human, get the move
         my_move = '-1'
         while not my_move.isnumeric() or int(my_move) not in valid_moves:
            print_message("Enter your move by index: ")
            my_move = getch(['0','1','2','3','4','5','6','7','8'])
            if not my_move.isnumeric():
               print_message("Invalid move!")
            elif my_move.isnumeric() and int(my_move) not in valid_moves:
               print_message("That space is taken!")
            else:
               move_index = int(my_move)

      else:
         if print_board_during_play:
            sleep(1)
         # If player is AI, get the move from the AI
         move_index = player_modules[turn].get_move(game_state['board'], symbols[turn])
      
      # Check if move is valid
      if move_index not in valid_moves:
         print_message(f"ERROR: {players[turn]}, {move_index} is not a valid move!")
         return (turn + 1) % 2
         break
      
      # Update board
      game_state['board'][move_index] = symbols[turn]
      game_state['moves_list'][turn].append(move_index)
      
      valid_moves.remove(move_index)
      
      # Check winner
      winner = get_winner(game_state['board'])

   if print_board_during_play:
      draw_main_board(players)   
   
   if winner != '':
      return turn
   
   return -1

def play_many_games(num_games, players, wins):
   for i in range(num_games):
      print_message('game: ' + str(i))
      print_status_bar(i, num_games)
      
      winner = play_game(players, False)
      if winner == -1:
         wins[2] += 1
      else:
         wins[winner] += 1

def print_status_bar(val, total_val):
   global global_stdscr
   row = board_offset_y + 10
   col = board_offset_x
   
   global_stdscr.move(row, col)
   global_stdscr.deleteln()

   number_of_boxes = 40
   val_boxes = int((val / total_val) * number_of_boxes)
   remainder = max(0, (number_of_boxes - val_boxes))
   val_box_str = ''
   if val_boxes > 1:
      val_box_str = '█' * val_boxes
   remainder_str = ''
   if remainder > 1:
      remainder = '░' * remainder
   global_stdscr.addstr(row, col, val_box_str + remainder_str)
   global_stdscr.refresh()

def main(stdscr):
   curses.start_color()
   curses.use_default_colors()
   curses.noecho()
   curses.curs_set(False)
   curses.use_default_colors()
   for i in range(0, curses.COLORS):
      curses.init_pair(i + 1, i, -1)
   
   global global_stdscr
   global_stdscr = stdscr
   
   player_files = load_player_files()     
   # Main Loop
   draw_main_menu()
      
   selection = 'noop'

   while selection and selection.lower() != 'q':
      players = []
      selection = getch(['1', '2', '3', 'q'])
      
      if selection == '1':
         if len(player_files) < 1:
            print_message("There are no AI's in the 'players' folder to play against")
            continue
         
         draw_letter_select_menu()

         letter = getch(['x','o'])
         computer_letter = 'X' if letter == 'o' else 'O'
         # print(f"OK, you will play '{letter.upper()}'.")
         players.append('Human')
         # Play against a single custom AI
         ai_player = get_ai_selection(player_files, computer_letter)

         # Make sure to place the 'X' first in the list
         if computer_letter == 'O':
            players.append(ai_player)
         else:
            players.insert(0, ai_player)
         
         winner = play_game(players)
         # Print winner
         if winner == -1:
            print_message("Cat's Game! No winner.")
         else:
            print_message(f"{get_printable_name(players[winner])} as {symbols[winner]}, is the Winner!")
         print_message("Press <C> to continue...", 2)
         pause = getch(['c'])

      elif selection == '2':
         if len(player_files) < 1:
            print_message("There are no AI's in the 'players' folder to play against")
            continue
         
         draw_num_games_menu()
         sub_selection = getch(['1', '2'])
         
         if sub_selection == '1':

            # Play two custom AI's against each other
            first_player = get_ai_selection(player_files, 'X')
            print_message(f"X: {get_printable_name(first_player)}")
            players.append(first_player)

            players.append(get_ai_selection(player_files, 'O'))
               
            play_game(players)
            print_message("Press <C> to continue...", 2)
            pause = getch(['c'])
         elif sub_selection == '2':
            if len(player_files) < 1:
               print_message("There are no AI's in the 'players' folder to play against")
               continue
            num_games = 5000
            wins = [0, 0, 0]
            
            # Play two custom AI's against each other
            players.append(get_ai_selection(player_files, 'X'))
            # print_message(f"{get_printable_name(players[0])} will be 'X'")
            players.append(get_ai_selection(player_files, 'O'))
               
            play_many_games(num_games, players, wins)
            
            # print(f"Games: {num_games}")
            # print(f"{get_printable_name(players[0])} as 'X' Wins: {wins[0]}")
            # print(f"{get_printable_name(players[1])} as 'O' Wins: {wins[1]}")
            # print(f"Ties: {wins[2]}")

            players2 = players[::-1]
            wins2 = [0, 0, 0]
            
            play_many_games(num_games, players2, wins2)
            
            # print(f"Games: {num_games}")
            # print(f"{get_printable_name(players[0])} as 'X' Wins: {wins[0]}")
            # print(f"{get_printable_name(players[1])} as 'O' Wins: {wins[1]}")
            # print(f"Ties: {wins[2]}")
            draw_many_game_results()
            print_many_games_scores(players, wins, wins2)
            print_message("Press <C> to continue...")
            pause = getch(['c'])

      elif selection == 'q':
         break
      draw_main_menu()

curses.wrapper(main)
