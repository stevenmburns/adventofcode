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

        logging.info( f"{level+1} {best_keys} {len(all_keys)}: {len(reached)} {len(frontier)} {''.join(str(x) for x in frontier)}")

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

def main2(fp):
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

    irow,icol = list(start)[0]
    p0 = irow+1,icol+1
    p1 = irow-1,icol+1
    p2 = irow+1,icol-1
    p3 = irow-1,icol-1

    new_board = []
    for jrow,line in enumerate(board):
        new_line = ''
        for jcol,c in enumerate(line):
            p = jrow, jcol
            if p in [ (irow-1,icol), (irow,icol-1), (irow+1, icol), (irow, icol+1)]:
                new_line += '#'
            elif p in [ (irow-1,icol-1), (irow+1,icol-1), (irow+1, icol+1), (irow-1, icol+1)]:
                new_line += '@'
            elif p == (irow,icol):
                new_line += '#'
            else:
                new_line += c
        new_board.append(new_line)

    board = new_board

    state = frozenset(), (p0,p1,p2,p3)

    reached = set()
    frontier = set( [state])
    level = 0

    best_keys = 0

    while frontier:

        logging.info( f"{level+1} {best_keys} {len(all_keys)}: {len(reached)} {len(frontier)}")

        new_frontier = set()
        for state in frontier:
            keys_acquired, ps = state


            for idx in range(len(ps)):
                irow,icol = ps[idx]
                dirs = [(-1,0),(1,0),(0,-1),(0,1)]

                ps_lst = list(ps)
                for drow,dcol in dirs:
                    jrow,jcol = irow+drow,icol+dcol
                    ps_lst[idx] = (jrow,jcol)
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

                            new_frontier.add( (frozenset( new_keys_acquired), tuple(ps_lst)))
                        else:
                            new_frontier.add( ( keys_acquired, tuple(ps_lst)))

        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)
        level += 1

    return None

@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 8 == main(fp)

@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 86== main(fp)

@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        assert 132 == main(fp)

@pytest.mark.skip
def test_A3():
    with open("data3","rt") as fp:
        assert 136 == main(fp)

@pytest.mark.skip
def test_A4():
    with open("data4","rt") as fp:
        assert 81 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        assert 3216 == main(fp)

#@pytest.mark.skip
def test_AA0():
    with open("dataP2_0","rt") as fp:
        assert 8 == main2(fp)

#@pytest.mark.skip
def test_AA1():
    with open("dataP2_1","rt") as fp:
        assert 24 == main2(fp)

#@pytest.mark.skip
def test_AA2():
    with open("dataP2_2","rt") as fp:
        assert 32 == main2(fp)

#@pytest.mark.skip
def test_AA3():
    with open("dataP2_3","rt") as fp:
        assert 72 == main2(fp)


@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print( main2(fp))




