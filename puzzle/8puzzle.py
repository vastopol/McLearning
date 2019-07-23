#!/usr/bin/python

# python 2.7
# 8 tile puzzle solver

# ----------------------------------------

# Modules
import itertools    # flatten n-dim matrix
import copy         # for deepcopy
import operator     # to sort by attributes of objects
import time

# Global Variables
default_puzzle = [[1,2,3], [4,0,6], [7,5,8]]

# Classes
class  node:
        def __init__(self, state, parent=None, g=0, h=0, f=0):
            self.state  = state   # 8 tile puzzle
            self.parent = parent
            self.g = g            # cost
            self.h = h            # heuristic
            self.f = f            # f = g + h

# ----------------------------------------

# program start point
def main():
    my_puzzle = [[-1,-2,-3], [-4,-5,-6], [-7,-8,-9]]
    print("The 8-Puzzle Solver")
    my_puzzle = setup_puzzle(my_puzzle)
    print_puzzle(my_puzzle)
    print("Enter your choice of algorithm")
    print("1. Uniform Cost Search")
    print("2. A* with Misplaced Tile Heuristic")
    print("3. A* with Manhattan Distance Heuristic")
    algo = input()
    if algo in [1,2,3]:
        start = time.clock()
        nlist = gsearch(my_puzzle, algo)
        end = time .clock
        if nlist:
            print("Solution Depth: ", nlist[0].g)
            print("Nodes Expanded: ", nlist[1])
            print("Max Queue Size: ", nlist[2])
            print("Time: " + str(fin-start) + " sec\n")
        else:
            print("Result was None")
    else:
        print("Input Error")

# ----------------------------------------

# Moves and Goals

def goal_test():
    pass

def move_left(state, dictionary, parent, gv):
        pass

def move_right(state, dictionary, parent, gv):
        pass

def move_up(state, dictionary, parent, gv):
        pass

def move_down(state, dictionary, parent, gv):
        pass

def expand(node):
    pass

# ----------------------------------------

# Heuristics

# ----------------------------------------

# General Search

def gsearch(puzzle, algorithm):
    pass

# ----------------------------------------

# Utilities

def dictify(state):
    data = {}
    for i in range(3):
        for j in range(3):
            data[state[i][j]] = (i,j)

def print_puzzle(puzzle):
    pass

def setup_puzzle(puzzle):
    pass

# ----------------------------------------

# program start
if __name__ == '__main__':
    main()