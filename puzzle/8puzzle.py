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
class node:
        def __init__(self, state, parent=None, g=0, h=0, f=0):
            self.state  = state   # 8 tile puzzle
            self.parent = parent
            self.g = g            # cost
            self.h = h            # heuristic
            self.f = f            # f = g + h

# ----------------------------------------

# Starting Point
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
        end = time.clock()
        if nlist:
            print("Solution Depth: ", nlist[0].g)
            print("Nodes Expanded: ", nlist[1])
            print("Max Queue Size: ", nlist[2])
            print("Time: " + str(end-start) + " sec\n")
        else:
            print("Result was None")
    else:
        print("Input Error")

# ----------------------------------------

# Moves and Goals

def goal_test(state):
    if list(itertools.chain.from_iterable(state)) == [1,2,3,4,5,6,7,8,0]:
        return True

def move_left(state, dictionary, parent, g):
    position = dictionary[0]
    if position[1] == 0:
        return None
    new_state = copy.deepcopy(state)
    a = new_state[position[0]][position[1]]
    b = new_state[position[0]][position[1]-1]
    new_state[position[0]][position[1]] = b
    new_state[position[0]][position[1]-1] = a
    new_node = node(new_state)
    new_node.parent = parent
    new_node.g = g + 1
    return new_node

def move_right(state, dictionary, parent, g):
    position = dictionary[0]
    if position[1] == 2:
        return None
    new_state = copy.deepcopy(state)
    a = new_state[position[0]][position[1]]
    b = new_state[position[0]][position[1]+1]
    new_state[position[0]][position[1]] = b
    new_state[position[0]][position[1]+1] = a
    new_node = node(new_state)
    new_node.parent = parent
    new_node.g = g + 1
    return new_node

def move_up(state, dictionary, parent, g):
    position = dictionary[0]
    if position[0] == 0:
        return None
    new_state = copy.deepcopy(state)
    a = new_state[position[0]][position[1]]
    b = new_state[position[0]-1][position[1]]
    new_state[position[0]][position[1]] = b
    new_state[position[0]-1][position[1]] = a
    new_node = node(new_state)
    new_node.parent = parent
    new_node.g = g + 1
    return new_node

def move_down(state, dictionary, parent, g):
    position = dictionary[0]
    if position[0] == 2:
        return None
    new_state = copy.deepcopy(state)
    a = new_state[position[0]][position[1]]
    b = new_state[position[0]+1][position[1]]
    new_state[position[0]][position[1]] = b
    new_state[position[0]+1][position[1]] = a
    new_node = node(new_state)
    new_node.parent = parent
    new_node.g = g + 1
    return new_node

def expand(node):
    coord = dictify(node.state)
    nodeL = move_left(node.state, coord, node, node.g)
    nodeR = move_right(node.state, coord, node, node.g)
    nodeU = move_up(node.state, coord, node, node.g)
    nodeD = move_down(node.state, coord, node, node.g)
    new_nodes = [nodeL, nodeR, nodeU, nodeD]
    return new_nodes

# ----------------------------------------

# Heuristics

# Misplaced tiles
def misplaced_tiles(puzzle):
    i = 0
    flat = list(itertools.chain.from_iterable(puzzle))
    if flat[0] != 1:
        i += 1
    if flat[1] != 2:
        i += 1
    if flat[2] != 3:
        i += 1
    if flat[3] != 4:
        i += 1
    if flat[4] != 5:
        i += 1
    if flat[5] != 6:
        i += 1
    if flat[6] != 7:
        i += 1
    if flat[7] != 8:
        i += 1
    return i

# Manhattan distance
# row div, col mod
def manhattan_distance(puzzle):
    total = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0:
                dx = (puzzle[i][j]-1)/3
                dy = (puzzle[i][j]-1)%3
                total += abs(i-dx) + abs(j-dy)
    return total

# ----------------------------------------

# General Search

def gsearch(puzzle, algorithm):
    num_exp = 0
    q_size = 0
    q = []      # frontier - queue of nodes
    seen = {}   # visited  - hash table of seen nodes
    root = node(puzzle)
    q.append(root)
    print("Starting")
    while True:
        if len(q) == 0:         # check for empty queue
            print("Failed")
            return None
        tempn = q.pop(0)        # dequeue, then add to seen
        seen[str(list(itertools.chain.from_iterable(tempn.state)))] = 1
        if goal_test(tempn.state):
            print_puzzle(tempn.state)
            print("Success\n")
            return [tempn, num_exp, q_size]
        print_puzzle(tempn.state)
        print("Expanding node with g(n) ", tempn.g, "h(n) ", tempn.h)
        new_nodes = expand(tempn)   # get list of all expanded states
        num_exp += 1
        for i in new_nodes:
            # check not null, not in hash
            if i != None and str(list(itertools.chain.from_iterable(i.state))) not in seen:
                if algorithm == 2:
                    i.h = misplaced_tiles(i.state)
                if algorithm == 3:
                    i.h = manhattan_distance(i.state)
                i.f = i.g + i.h
                q.append(i)
                # add to seen states
                seen[str(list(itertools.chain.from_iterable(i.state)))] = 1
                q = sorted(q, key=operator.attrgetter('f'))     # sort low to high
                if len(q) > q_size:
                    q_size = len(q)

# ----------------------------------------

# Utilities

def dictify(state):
    data = {}
    for i in range(3):
        for j in range(3):
            data[state[i][j]] = (i,j)
    return data

def print_puzzle(puzzle):
    print
    for i in puzzle:
        print(i)
    print

def setup_puzzle(puzzle):
    ival = input("Type 1 to use default puzzle or 2 to enter your own puzzle.\n")
    if ival == 2:
        print("Enter your puzzle, use zero for blank, use spaces or tabs between numbers")
        for r in range(len(puzzle)):
            print("Enter row %d" % int(r+1))
            ival = filter(str.strip, list(raw_input()))
            # should be 3 single digit integers per line
            if not len(ival) == len(puzzle[0]):
                print("Entry error, default selected")
                return default_puzzle
            for i in range(len(ival)):
                puzzle[r][i] = int(ival[i])
        # should be [0,1,2,3,4,5,6,7,8]
        flat = list(set(itertools.chain.from_iterable(puzzle)))
        if not flat == range(9):
            print("Entry error, default selected")
            return default_puzzle
        return puzzle
    elif ival == 1:
        print("default selected")
        return default_puzzle
    else:
        print("Entry error, default selected")
        return default_puzzle

# ----------------------------------------

# Start
if __name__ == '__main__':
    main()
