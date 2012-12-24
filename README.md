pySudoku
========

Simple Sudoku solver created in Python.

About
-----
First the program scans each cell and if there exists only one possibility, then it inserts that number. The program does this until the puzzle is stuck. Then it runs a backtracking DFS search to "try out" the possibilities, eliminating those (and its children) that doesn't work.

I aimed for code readability and simplicity over running time, although this program can solve each Sudoku puzzle in ~200 ms which isn't too shabby.

How to run
----------
python pySudoku.py Sudokus.txt

Of course, you can use this program with any text file that contains Sudoku puzzles.
