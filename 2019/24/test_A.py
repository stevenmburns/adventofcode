import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import heapq

logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append(list(line))

    return seq

def step( board):
    nrows = len(board)
    ncols = len(board[0])
    
    new_board = []
    for irow, line in enumerate(board):
        new_line = ''
        for icol, c in enumerate(line):
            count = 0
            for drow,dcol in [(-1,0),(1,0),(0,-1),(0,1)]:
                jrow,jcol = irow+drow,icol+dcol
                if 0 <= jrow < nrows and 0 <= jcol < ncols:
                    if board[jrow][jcol] == '#':
                        count += 1

            if c == '#' and count != 1:
                new_c = '.'
            elif c == '.' and count in [1,2]:
                new_c = '#'
            else:
                new_c = c
            new_line += new_c
        new_board.append(list(new_line))

    return new_board


def print_board(board):
    print()
    for line in board:
        print(line)

def score(board):
    ncols = len(board[0])
    result = 0
    for irow, line in enumerate(board):
        for icol, c in enumerate(line):
            if c == '#':
                result |= 1 << (ncols*irow + icol) 
    return result

def make_immutable(board):
    return tuple( tuple(line) for line in board)

def main(fp):
    board = parse(fp)

    boards = set()
    boards.add( make_immutable(board))

    for _ in range(10000):
        board = step(board)

        immutable_board = make_immutable(board)

        if immutable_board in boards:
            break

        boards.add( immutable_board)

    print_board(board)

    return score(board)

def count_bugs( board):
    count = 0
    for irow,line in enumerate(board):
        for icol,c in enumerate(line):
            if type(c) == str:
                if c == '#':
                    count += 1
            else:
                count += count_bugs( c)
    return count

def count2( board, p, north, east, south, west):
    nrows = len(board)
    ncols = len(board[0])

    (irow, icol) = p
    count = 0
    for drow,dcol in [(-1,0),(1,0),(0,-1),(0,1)]:
        jrow,jcol = irow+drow,icol+dcol
        if 0 <= jrow < nrows and 0 <= jcol < ncols:
            c = board[jrow][jcol] 
            if type(c) == str:
                if c == '#': count += 1
            else:
                if   (drow,dcol) == (-1,0): #north
                    count += sum(1 for i in range(5) if c[-1][i] == '#')
                elif (drow,dcol) == (0,1): #east
                    count += sum(1 for i in range(5) if c[i][0] == '#')
                elif (drow,dcol) == (1,0): #south
                    count += sum(1 for i in range(5) if c[0][i] == '#')
                elif (drow,dcol) == (0,-1): #west
                    count += sum(1 for i in range(5) if c[i][-1] == '#')
                else:
                    assert False
        elif jrow == -1:
            if north == '#': count += 1
        elif jcol == -1:
            if west == '#': count += 1
        elif jrow == nrows:
            if south == '#': count += 1
        elif jcol == ncols:
            if east == '#': count += 1
        else:
            assert False, (jrow,jcol)


    return count


def test_count2():
    txt = """#.#.#
.#.#.
#.#.#
.#.#.
#.#.#"""
    board = [list(line) for line in txt.split('\n')]
    print(board)
    print_board2(board)

    assert 0 == count2( board, p=(2,2), north='.', east='.', south='.', west='.')
    assert 4 == count2( board, p=(1,2), north='.', east='.', south='.', west='.')
    assert 0 == count2( board, p=(0,2), north='.', east='.', south='.', west='.')
    assert 3 == count2( board, p=(0,1), north='.', east='.', south='.', west='.')
    assert 4 == count2( board, p=(0,1), north='#', east='.', south='.', west='.')
    assert 1 == count2( board, p=(0,0), north='#', east='.', south='.', west='.')
    assert 2 == count2( board, p=(0,0), north='#', east='.', south='.', west='#')
    assert 2 == count2( board, p=(0,4), north='#', east='#', south='.', west='.')
    assert 2 == count2( board, p=(4,4), north='.', east='#', south='#', west='.')
    assert 2 == count2( board, p=(4,0), north='.', east='.', south='#', west='#')

def test_count2_dn():
    txt = """#.#.#
.#.#.
#.#.#
.#.#.
#.#.#"""
    board = [list(line) for line in txt.split('\n')]
    board[2][2] = [list(line) for line in txt.split('\n')]
    print(board)
    print_board2(board)

    assert 0 == count2( board, p=(2,2), north='.', east='.', south='.', west='.')
    assert 6 == count2( board, p=(1,2), north='.', east='.', south='.', west='.')
    assert 6 == count2( board, p=(3,2), north='.', east='.', south='.', west='.')

    return

    assert 0 == count2( board, p=(0,2), north='.', east='.', south='.', west='.')
    assert 3 == count2( board, p=(0,1), north='.', east='.', south='.', west='.')
    assert 4 == count2( board, p=(0,1), north='#', east='.', south='.', west='.')
    assert 1 == count2( board, p=(0,0), north='#', east='.', south='.', west='.')
    assert 2 == count2( board, p=(0,0), north='#', east='.', south='.', west='#')
    assert 2 == count2( board, p=(0,4), north='#', east='#', south='.', west='.')
    assert 2 == count2( board, p=(4,4), north='.', east='#', south='#', west='.')
    assert 2 == count2( board, p=(4,0), north='.', east='.', south='#', west='#')

    



def step2( board, north, east, south, west):
    
    new_board = []
    for irow, line in enumerate(board):
        new_line = []
        for icol, c in enumerate(line):

            count = count2( board, (irow,icol), north, east, south, west)

            if type(c) == str:
                if c == '#' and count != 1:
                    new_c = '.'
                elif c == '.' and count in [1,2]:
                    if (irow,icol) != (2,2):
                        new_c = '#'
                    else:
                        c = [ ['.' for _ in range(5)] for _ in range(5)]
                        new_c = step2( c, board[irow-1][icol], board[irow][icol+1],
                                       board[irow+1][icol], board[irow][icol-1])
                else:
                    new_c = c
            else:
                assert (irow,icol) == (2,2)
                new_c = step2( c, board[irow-1][icol], board[irow][icol+1],
                               board[irow+1][icol], board[irow][icol-1])

            new_line.append(new_c)
        new_board.append(new_line)

    return new_board


def print_board2( board, level=0):
    print(f'===={level}====')
    for line in board:
        print( ''.join( '?' if type(c) != str else c for c in line))

    c = board[2][2]
    if type(c) != str:
        print_board2( c, level+1)


def main2(fp,n=200):
    board = parse(fp)

    print_board2(board)

    for i in range(n):
        c = [ ['.' for _ in range(5)] for _ in range(5)]
        c[2][2] = board
        board = step2(c, north='.', east='.', south='.', west='.')
        print(f'After step {i+1}')
        all_empty = all( x == '.' for icol,line in enumerate(board) for irow,x in enumerate(line) if (irow,icol) != (2,2))
        if all_empty:
            board = board[2][2]

        print_board2( board)

    return count_bugs(board)

@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 2129920 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open("data0","rt") as fp:
        assert 99 == main2(fp,n=10)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))

