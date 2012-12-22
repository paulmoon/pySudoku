# Paul Moon
# December 2012
# pySudoku.py

import fileinput

def solve(s):
    pass

def main():
    s = []
    count = 0

    for line in fileinput.input():
        # Assumes Sudokus are separated by an empty line
        if line not in ['\n', '\r\n']:
             s.append(line)
        else:
            solve(s)
            s = []

if __name__ == "__main__":
    main()