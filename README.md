# curriculum-tictactoe

A TicTacToe AI testing framework.

## Usage

To use this framework to test your Tic-Tac-Toe A.I., you will first need to code your A.I. using the following specifications:

1. **Name** of your file. The name of the file will become the name of the AI in the testing framework, so choose wisely. The name will be generated from the filename by removing the `.py`, replacing underscores `_` with spaces, and **title-casing** the remaining string. So, `the_underdog.py` would become `The Underdog`.
2. Your AI file should implement a top-level function called `get_move(board, letter)` that accepts two parameters:
   a. `board`: The current state of a tic-tac-toe board represented by a list of 9 strings, with each string being one of `'X'`, `'O'`, or `''`.
   b. `letter`: The letter of the player to move next. This will be either `'X'` or `'O'`.
3. Your `get_move` function should return an integer representing the **index** of the space to place the move. For example, if the AI _decides_ to place its letter in the center square, it would return `4`.
4. Your AI file should be placed in the `/players` folder.

## Board Layout

The testing framework represents the **board** as a list of strings, with **9** elements. The indexes of the elements are laid out as:

```
 0 │ 1 │ 2
───┼───┼───
 3 │ 4 │ 5
───┼───┼───
 6 │ 7 │ 8
```

## Run

To run the code, you will need to first to create a virtual environment using `pipenv shell`, then run `pipenv install` to install the necessary modules.
Then, run `python main.py`
