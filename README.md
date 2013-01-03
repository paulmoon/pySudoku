pySudoku
========

Simple Sudoku solver/generator created in Python.

About
-----

Solver: First the program scans each cell and if there exists only one possibility, then it inserts that number. The program does this until the puzzle is stuck. Then it runs a backtracking DFS search to "try out" the possibilities, eliminating those (and its children) that doesn't work.

I aimed for code readability and simplicity over running time, although this program can solve a Sudoku puzzle in ~0.2s on average.

Generator: The generator starts with an empty 9x9 grid and fills it up by iterating from the top left cell to the bottom right, and filling in the cells by trying random numbers. It checks if the inserted number works, and if so, continue on recursively. Then the full 9x9 grid is reduced down so that it becomes the start of a Sudoku puzzle. It generates a list of integers 0-80 representing the indices in the puzzle, then scrambles the order. To reduce, we try to remove the number at the first index in the list and then attempting to solve the puzzle. If there exists more than one solution, then it is not a valid Sudoku puzzle, so undo the last change. If easy puzzles are desired, then after a puzzle with a unique solution is found, algorithm stops. If difficult puzzles are wanted, then even after a valid puzzle is found, all the remaining indices are tried to see if the puzzle can be made any harder. The difficult puzzles are not only unique boards, but boards where you cannot remove any more numbers without destroying the uniqueness of the solution.

How to run
----------
To run the solver:
    python pySudoku.py Sudokus.txt

To run the generator:
    python Generator.py

Of course, you can use the solver with any text file that contains Sudoku puzzles.
The generator writes to a file named "SudokuPuzzles.txt", with each puzzle being represented as one line of integers read from the top left to the bottom right of the grid.