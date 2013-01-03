""" Name: pySudoku.py
    Author: Paul Moon
    Date: December 2012

    Description:
    Solves Sudoku puzzles!
    
    First try to solve by filling in the cells with only one possibility.
    If it cannot go any further, use a backtracking DFS (depth-first search)
    algorithm to try the possible solutions. As soon as a solution is found,
    it terminates the algorithm and prints it out.

    The algorithm assumes that empty cells are denoted with a 0.
"""

import fileinput
import time

def print_sudoku(s):
    """ Formats the Sudoku puzzle currently in a 2D list into
    a grid with lines separating the blocks for readability """
    for row in range(9):
        for col in range(9):
            print s[row][col],
            if (col+1) == 3 or (col+1) == 6:
                print " | ",
        if (row+1) == 3 or (row+1) == 6:
            print "\n" + "-"*25,
        print
    print

def test_cell(s, row, col):
    """ Given a Sudoku puzzle s, row, and column number, return a list which represents
    the valid numbers that can go in that cell. 0 = possible, 1 = not possible """
    used = [0]*10
    used[0] = 1
    block_row = row / 3
    block_col = col / 3

    # Row and Column
    for m in range(9):
        used[s[m][col]] = 1;
        used[s[row][m]] = 1;

    # Square
    for m in range(3):
        for n in range(3):
            used[s[m + block_row*3][n + block_col*3]] = 1

    return used

def initial_try(s):
    """ Given a Sudoku puzzle, try to solve the puzzle by iterating through each
    cell and determining the possible numbers in that cell. If only one possible
    number exists, fill it in and continue on until the puzzle is stuck. """
    stuck = False

    while not stuck:
        stuck = True
        # Iterate through the Sudoku puzzle
        for row in range(9):
            for col in range(9):
                used = test_cell(s, row, col)
                # More than one possibility
                if (used.count(0) != 1):
                    continue

                for m in range(1, 10):
                    # If current cell is empty and there is only one possibility
                    # then fill in the current cell
                    if (s[row][col] == 0 and used[m] == 0):
                        s[row][col] = m
                        stuck = False
                        break

def DFS_solve(s, row, col):
    """ Given a Sudoku puzzle, solve the puzzle by recursively performing DFS
    which 'tries' out the possible solutions and by using backtracking (eliminating 
    invalid tries and all the possible cases arising from those tries) """
    if row == 8 and col == 8:
        used = test_cell(s, row, col)
        if 0 in used:
            s[row][col] = used.index(0)
        return True

    if col == 9:
        row = row+1
        col = 0

    if (s[row][col] == 0):
        used = test_cell(s, row, col)
        for i in range(1, 10):
            if (used[i] == 0):
                s[row][col] = i
                if (DFS_solve(s, row, col+1)):
                    return True

        # Reached here? Then we tried 1-9 without success
        s[row][col] = 0
        return False

    return DFS_solve(s, row, col+1)

def main():
    start = time.time()
    num_puzzles = 0
    s = []
    text = ""

    for line in fileinput.input():
        line = ' '.join(line.split())
        text += line

    while (len(text) > 0):
        l = []

        # Get a row of numbers
        while len(l) < 9:
            if text[0].isdigit():
                l.append(int(text[0]))
            text = text[1:]

        # Insert that row into the Sudoku grid
        s.append(l)

        if len(s) == 9:
            num_puzzles += 1
            print "Puzzle Number %d:\n" %(num_puzzles)
            print "Original:"
            print_sudoku(s)

            initial_try(s)
            for line in s:
                if 0 in line:
                    DFS_solve(s, 0, 0)
                    break

            print "Solution:"
            print_sudoku(s)

            print "="*30
            s = []

    print "%d seconds to solve %d puzzles" %(time.time() - start, num_puzzles)

if __name__ == "__main__":
    main()