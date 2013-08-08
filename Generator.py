"""
Name: Generator.py
Author: Paul Moon
Date: December 2012

Description:
Generates Sudoku puzzles that have a unique solution.
Able to generate either easy (requires nothing harder than hidden singles) puzzles,
or medium/difficult puzzles (sometimes requiring extreme strategies/techniques like
cell-forcing chains).

The algorithm that generates difficult puzzles gives you not only unique boards,
but boards where you cannot remove any more numbers without destroying the uniqueness
of the solution.
"""

import pySudoku
import random
import time

def toString(s):
    """
    Formats a 2D list Sudoku puzzle into one line of integers
    for easy writing to a file
    """
    output = ""
    for i in range(9):
        for j in range(9):
            output += str(s[i][j])
    return output + "\n"

def checkValid(s, row, col):
    """
    Returns True if a given cell is valid in a Sudoku puzzle, and
    False if not. A cell is valid if the number in that cell is not present
    in any of the cells in the same row, or the same column, or the same block.
    """
    block_row = row // 3
    block_col = col // 3

    # Row and Column
    # Ignore blank spots
    for m in range(9):
        if s[row][m] != 0 and m != col and s[row][m] == s[row][col]:
            return False
        if s[m][col] != 0 and m != row and s[m][col] == s[row][col]:
            return False

    # Block
    for m in range(3):
        for n in range(3):
            newRow = m + block_row*3
            newCol = n + block_col*3
            if s[newRow][newCol] != 0 and newRow != row and newCol != col\
            and s[newRow][newCol ] == s[row][col]:
                return False

    return True

def populateBoard(s, row, col):
    """
    Starting with a 9x9 grid of 0's, this function recursively populates
    the grid. It makes a list of integers from 1-9, shuffles the order, and
    tries the first number in the list in the current cell. If the inserted
    integer works, then it continues on. If the integer does not work then
    it tries the next one in the list. If none of the integers work, then
    set it to blank and return false.
    """
    if row == 8 and col == 8:
        used = pySudoku.test_cell(s, row, col)
        s[row][col] = used.index(0)
        return True

    if col == 9:
        row = row+1
        col = 0

    temp = list(range(1, 10))
    random.shuffle(temp)
    # Fill Sudoku
    for i in range(9):
        s[row][col] = temp[i]
        if checkValid(s, row, col):
            if populateBoard(s, row, col+1):
                return True
    s[row][col] = 0
    return False

def DFS_solve(copy_s, row, col):
    """
    Recursively solves the copy_s puzzle with a backtracking
    DFS algorithm, while returning the number of solutions found.
    Starts at row 0 and column 0, and continues on to the right and
    down the rows.
    """
    num_solutions = 0

    # Reached the last cells without any error, so there is a solution
    if row == 8 and col == 8:
        return num_solutions + 1

    if col == 9:
        row = row+1
        col = 0

    if copy_s[row][col] == 0:
        # Used = list of size 10 representing which numbers are possible
        # in the puzzle. 0 = possible, 1 = not possible. Ignore index 0.
        used = pySudoku.test_cell(copy_s, row, col)
        # No possible solutions. Return 0 for number of solutions
        if 0 not in used:
            return 0

        while 0 in used:
            copy_s[row][col] = used.index(0)
            used[used.index(0)] = 1
            num_solutions += DFS_solve(copy_s, row, col+1)

        # Reached here? Then we tried 1-9 without success
        copy_s[row][col] = 0
        return num_solutions

    num_solutions += DFS_solve(copy_s, row, col+1)
    return num_solutions

def reduce_sudoku(s, difficulty):
    """
    First generate a list of integers 0-80 representing the indices
    in the puzzle. Scramble the order. Given a complete Sudoku puzzle s,
    try to remove the number at the first index in the list and then attempting
    to solve it. If there exists more than one solution, then it is not a valid
    Sudoku puzzle, so undo the last change. If easy puzzles are desired, then
    after a puzzle with a unique solution is found, algorithm stops. If difficult
    puzzles are wanted, then even after a valid puzzle is found, all the remaining
    indices must be tried to see if the puzzle can be made any harder.
    """
    indices = list(range(81))
    random.shuffle(indices)

    while indices:
        row = indices[0] // 9
        col = indices[0] % 9
        temp = s[row][col]
        s[row][col] = 0
        indices = indices[1:]

        copy_s = [l[:] for l in s]

        pySudoku.initial_try(copy_s)

        for line in copy_s:
            if 0 in line:
                num_solutions = DFS_solve(copy_s, 0, 0)
                # Not a puzzle with a unique solution, so undo the last insertion
                if num_solutions > 1:
                    s[row][col] = temp
                    # If we want easy puzzles, we would stop here after finding
                    # the first puzzle with a unique solution without attempting to
                    # make it harder by trying to remove other elements and seeing
                    # if there is another harder puzzle with a unique solution
                    if difficulty == "E" or difficulty == "e":
                        return
                break

    return

def main():
    f = open("SudokuPuzzles.txt", "w")
    user_input = int(input("How many Sudoku puzzles would you like to generate?: "))
    difficulty = input("Easy or Difficult puzzles?: (e or d)")
    start = time.time()

    for _ in range(user_input):
        # 9 x 9 grid of 0s
        s = [[0]*9 for _ in range(9)]

        populateBoard(s, 0, 0)
        reduce_sudoku(s, difficulty)
        output = toString(s)
        f.write(output)

    print("{:.2f} seconds to come up with {} Sudoku puzzles.".format(time.time() - start, user_input))

if __name__ == '__main__':
    main()
