
import io
import pytest

import logging
from logging import debug
import re

from collections import deque
from copy import deepcopy

#logging.basicConfig(level=logging.DEBUG)

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(list(line))
    return seq

def adjacent( board, r, c):
    nrows = len(board)
    ncols = len(board[0])


    count = 0
    if r-1 >= 0:
        if c-1 >= 0 and board[r-1][c-1] == '#': count += 1
        if board[r-1][c] == '#': count += 1
        if c+1 < ncols and board[r-1][c+1] == '#': count += 1
    if True:
        if c-1 >= 0 and board[r][c-1] == '#': count += 1
        if c+1 < ncols and board[r][c+1] == '#': count += 1

    if r+1 < nrows:
        if c-1 >= 0 and board[r+1][c-1] == '#': count += 1
        if board[r+1][c] == '#': count += 1
        if c+1 < ncols and board[r+1][c+1] == '#': count += 1
    return count

def adjacent2( board, r, c):
    nrows = len(board)
    ncols = len(board[0])

    def occupied_in_direction( delta_r, delta_c):
        rr = r
        cc = c
        while True:
            rr, cc = rr + delta_r, cc + delta_c
            if 0 <= rr < nrows and 0 <= cc < ncols:
                if board[rr][cc] == 'L':
                    return False
                elif board[rr][cc] == '#':
                    return True
            else:
                return False

    count = 0
    if occupied_in_direction( -1, -1): count += 1
    if occupied_in_direction( -1,  0): count += 1
    if occupied_in_direction( -1,  1): count += 1
    if occupied_in_direction(  0, -1): count += 1

    if occupied_in_direction(  0,  1): count += 1
    if occupied_in_direction(  1, -1): count += 1
    if occupied_in_direction(  1,  0): count += 1
    if occupied_in_direction(  1,  1): count += 1
    return count


def step( board):
    new_board = deepcopy(board)

    nrows = len(board)
    ncols = len(board[0])

    for r in range(nrows):
        for c in range(ncols):
            if board[r][c] == '.':
                pass
            elif board[r][c] == 'L':
                if adjacent( board, r, c) == 0:
                    new_board[r][c] = '#'
            elif board[r][c] == '#':
                if adjacent( board, r, c) >= 4:
                    new_board[r][c] = 'L'
            else:
                assert False, (r,c,board[r][c])


    for line in new_board:
        for x in line:
            print(x,end='')
        print()


    return new_board

def step2( board):
    new_board = deepcopy(board)

    nrows = len(board)
    ncols = len(board[0])

    for r in range(nrows):
        for c in range(ncols):
            if board[r][c] == '.':
                pass
            elif board[r][c] == 'L':
                if adjacent2( board, r, c) == 0:
                    new_board[r][c] = '#'
            elif board[r][c] == '#':
                if adjacent2( board, r, c) >= 5:
                    new_board[r][c] = 'L'
            else:
                assert False, (r,c,board[r][c])


    for line in new_board:
        for x in line:
            print(x,end='')
        print()


    return new_board

 
def occupied( board):
    nrows = len(board)
    ncols = len(board[0])

    count = 0
    for r in range(nrows):
        for c in range(ncols):
            if board[r][c] == '#':
                count += 1
    print(count)
    return count

def main( fp):
    board = parse(fp)
    print(occupied(board))    
    for i in range(100):
        board = step(board)
        print(occupied(board))

    return occupied(board)

def main2( fp):
    board = parse(fp)
    print(occupied(board))    
    for i in range(100):
        board = step2(board)
        print(occupied(board))

    return occupied(board)

def test_occupied():
    board = [ ['#','.','L'],
              ['#','.','L'],
              ['#','.','L']]

    assert 3 == occupied(board)

def test_adjacent():
    board = [ ['#','.','L'],
              ['#','.','L'],
              ['#','.','L']]

    assert 1 == adjacent(board, 0, 0)
    assert 2 == adjacent(board, 1, 0)
    assert 1 == adjacent(board, 2, 0)
    assert 2 == adjacent(board, 0, 1)
    assert 3 == adjacent(board, 1, 1)
    assert 2 == adjacent(board, 2, 1)
    assert 0 == adjacent(board, 0, 2)
    assert 0 == adjacent(board, 1, 2)
    assert 0 == adjacent(board, 2, 2)



def test_A():
#    with open( "data0", "rt") as fp:
#        assert 37 == main(fp)
    with open( "data0", "rt") as fp:
        assert 26 == main2(fp)


def test_C():
#    with open( "data", "rt") as fp:
#        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))

