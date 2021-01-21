import sys
import pytest
import io
import re
import itertools
from collections import deque

import array

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append( line)

    assert all( len(seq[0]) == len(row) for row in seq[1:])

    return seq

def main(fp):
    seq = parse(fp)

    nrows = len(seq)
    ncols = len(seq[0])
    
    assert nrows % 2 == 1
    assert ncols % 2 == 1

    crow = (nrows-1)//2
    ccol = (ncols-1)//2

    infected = set()
    for irow,row in enumerate(seq):
        for icol,c in enumerate(row):
            if c == '#':
                infected.add( (irow,icol))
            
    cursor = (crow,ccol)
    dir = (-1,0)

    def turn_right():
        nonlocal dir
        if dir == (-1,0):
            dir = (0,1)
        elif dir == (0,1):
            dir = (1,0)
        elif dir == (1,0):
            dir = (0,-1)
        elif dir == (0,-1):
            dir = (-1,0)
        else:
            assert False, dir

    def turn_left():
        for _ in range(3):
            turn_right()

    count_infections = 0

    def burst():
        nonlocal cursor, count_infections
        if cursor in infected:
            turn_right()
        else:
            turn_left()

        if cursor not in infected:
            infected.add( cursor)
            count_infections += 1
        else:
            infected.remove( cursor)

        cursor = cursor[0] + dir[0], cursor[1] + dir[1]


    counts = [count_infections]
    for i in range(10000):
        burst()
        counts.append(count_infections)

    return counts


def main2(fp):
    seq = parse(fp)

    nrows = len(seq)
    ncols = len(seq[0])
    
    assert nrows % 2 == 1
    assert ncols % 2 == 1

    crow = (nrows-1)//2
    ccol = (ncols-1)//2

    """ clean (0) => weakened (1) => infected (2) => flagged (3) ==> clean (0)
"""

    state = {}
    for irow,row in enumerate(seq):
        for icol,c in enumerate(row):
            if c == '#':
                state[(irow,icol)] = 2
            
    cursor = (crow,ccol)
    dir = (-1,0)

    def turn_right():
        nonlocal dir
        if dir == (-1,0):
            dir = (0,1)
        elif dir == (0,1):
            dir = (1,0)
        elif dir == (1,0):
            dir = (0,-1)
        elif dir == (0,-1):
            dir = (-1,0)
        else:
            assert False, dir

    def turn_left():
        for _ in range(3):
            turn_right()

    def turn_back():
        for _ in range(2):
            turn_right()

    count_infections = 0

    def get_state( cursor):
        if cursor in state:
            return state[cursor]
        else:
            return 0

    def burst():
        nonlocal cursor, count_infections
        s = get_state(cursor)
        if s == 0:
            turn_left()
        elif s == 1:
            count_infections += 1
        elif s == 2:
            turn_right()
        elif s == 3:    
            turn_back()
        else:
            assert False, s

        state[cursor] = (s+1)%4

        cursor = cursor[0] + dir[0], cursor[1] + dir[1]


    counts = [count_infections]
    for i in range(10000000):
        if i % 100000 == 0:
            print(i)
        burst()
        counts.append(count_infections)

    return counts


@pytest.mark.skip
def test_A():
    with open("data0", "rt") as fp:
        counts = main(fp)
        assert 5 == counts[7]
        assert 41 == counts[70]
        assert 5587 == counts[10000]


@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        counts = main(fp)
        print(counts[10000])

#@pytest.mark.skip
def test_A():
    with open("data0", "rt") as fp:
        counts = main2(fp)
        assert 26 == counts[100]
        assert 2511944 == counts[10000000]

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        counts = main2(fp)
        print(counts[10000000])
