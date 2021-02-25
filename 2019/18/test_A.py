import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p = re.compile(r'^[@#.a-zA-Z]*$')

    for line in fp:
        line = line.rstrip('\n')
        assert p.match(line)
        seq.append( line)

    return seq

def main(fp):
    board = parse(fp)

    nrows = len(board)
    ncols = len(board[0])

    start = set()
    all_keys = set()
    for irow,line in enumerate(board):
        assert ncols == len(line)
        for icol,c in enumerate(line):
            if c == '@':
                start.add((irow,icol))
            if c.islower():
                all_keys.add( c)

    assert len(start) == 1

    state = frozenset(), list(start)[0]


    reached = set()
    frontier = set( [state])
    level = 0

    best_keys = 0

    while frontier:
        print( len(reached), len(frontier), best_keys, len(all_keys))

        new_frontier = set()
        for state in frontier:
            keys_acquired, (irow,icol) = state

            dirs = [(-1,0),(1,0),(0,-1),(0,1)]

            for drow,dcol in dirs:
                jrow,jcol = irow+drow,icol+dcol
                if 0 <= jrow < nrows and 0 <= jcol < ncols:
                    c = board[jrow][jcol]
                    if c == '#': continue
                    if c.isupper() and c.lower() not in keys_acquired: continue
                    if c.islower():
                        new_keys_acquired = set(keys_acquired)
                        new_keys_acquired.add( c)

                        if len(new_keys_acquired) > best_keys:
                            best_keys = len(new_keys_acquired)

                        if new_keys_acquired == all_keys:
                            return level+1

                        new_frontier.add( (frozenset( new_keys_acquired), (jrow,jcol)))
                    else:
                        new_frontier.add( ( keys_acquired, (jrow,jcol)))

        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)
        level += 1

    return None

#@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 8 == main(fp)

#@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 86== main(fp)

#@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        assert 132 == main(fp)

#@pytest.mark.skip
def test_A3():
    with open("data3","rt") as fp:
        assert 136 == main(fp)

#@pytest.mark.skip
def test_A4():
    with open("data4","rt") as fp:
        assert 81 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        assert 10632 == main(fp)




