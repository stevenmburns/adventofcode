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

    p = re.compile(r'^[@#.a-zA-Z]*$')

    for line in fp:
        line = line.rstrip('\n')
        assert p.match(line)
        seq.append( line)

    return seq

def determine_path_lengths( board, p):
    nrows = len(board)
    ncols = len(board[0])

    reached = set()
    frontier = set( [p])
    level = 0

    length_tbl = { p: 0}

    while frontier:

        new_frontier = set()
        for state in frontier:

            (irow,icol) = state

            dirs = [(-1,0),(1,0),(0,-1),(0,1)]

            for drow,dcol in dirs:
                jrow,jcol = irow+drow,icol+dcol
                if 0 <= jrow < nrows and 0 <= jcol < ncols:
                    c = board[jrow][jcol]
                    if c == '#': continue
                    if c != '.':
                        if (jrow,jcol) not in length_tbl:
                            length_tbl[ (jrow,jcol)] = level+1
                    else:
                        new_frontier.add( (jrow,jcol))

        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)
        level += 1
    
    return length_tbl


def main(fp):
    board = parse(fp)

    nrows = len(board)
    ncols = len(board[0])
 
    adjacents = {}

    start = set()
    all_keys = set()
    for irow,line in enumerate(board):
        assert ncols == len(line)
        for icol,c in enumerate(line):
            if c == '@':
                start.add((irow,icol))
            if c.islower():
                all_keys.add( c)

            if c == '@' or c.isupper() or c.islower():
                adjacents[ (irow,icol)] = determine_path_lengths(board, (irow,icol))

    print()
    for k,v in adjacents.items():
        print( k, board[k[0]][k[1]])
        for kk,vv in v.items():
            print( '\t', kk, board[kk[0]][kk[1]], vv)

    assert len(start) == 1

    state = frozenset(), list(start)[0]

    reached = {} # state => steps

    frontier = []
    heapq.heappush(frontier, (0, state))

    while frontier:

        level, state = heapq.heappop( frontier)

        print( f'headpop: {level} {state}') 

        if state not in reached:
            reached[state] = level

        keys_acquired, (irow,icol) = state

        for (jrow,jcol),cost in adjacents[(irow,icol)].items():
            new_cost = level + cost

            if (jrow,jcol) == (irow,icol): continue
 
            c = board[jrow][jcol]
            assert c != '#'
            if c.isupper() and c.lower() not in keys_acquired: continue
            if c.islower():
                new_keys_acquired = set(keys_acquired)
                new_keys_acquired.add( c)

                if new_keys_acquired == all_keys:
                    return new_cost

                new_state = (frozenset( new_keys_acquired), (jrow,jcol))
            else:
                new_state = (keys_acquired, (jrow,jcol))


            if new_state not in reached or reached[new_state] > new_cost:
                reached[new_state] = new_cost
                heapq.heappush( frontier, (new_cost,new_state))





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


    adjacents = {}
    for irow,line in enumerate(board):
        assert ncols == len(line)
        for icol,c in enumerate(line):
            if c == '@' or c.isupper() or c.islower():
                adjacents[ (irow,icol)] = determine_path_lengths(board, (irow,icol))

    print()
    for k,v in adjacents.items():
        print( k, board[k[0]][k[1]])
        for kk,vv in v.items():
            print( '\t', kk, board[kk[0]][kk[1]], vv)


    state = frozenset(), (p0,p1,p2,p3)


    reached = {} # state => steps

    frontier = []
    heapq.heappush(frontier, (0, state))

    while frontier:

        level, state = heapq.heappop( frontier)

        logging.info( f'headpop: {level} {len(state[0])}') 

        if state not in reached:
            reached[state] = level

        keys_acquired, ps = state

        for idx in range(len(ps)):
            irow,icol = ps[idx]
            
            for (jrow,jcol),cost in adjacents[(irow,icol)].items():
                new_ps = list(ps)
                new_ps[idx] = (jrow,jcol)
                new_ps = tuple(new_ps)

                new_cost = level + cost

                if (jrow,jcol) == (irow,icol): continue

                c = board[jrow][jcol]
                assert c != '#'

                if c.isupper() and c.lower() not in keys_acquired: continue
                if c.islower():
                    new_keys_acquired = set(keys_acquired)
                    new_keys_acquired.add( c)

                    if new_keys_acquired == all_keys:
                        return new_cost

                    new_state = (frozenset( new_keys_acquired), new_ps)
                else:
                    new_state = (keys_acquired, new_ps)


                if new_state not in reached or reached[new_state] > new_cost:
                    reached[new_state] = new_cost
                    heapq.heappush( frontier, (new_cost,new_state))



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


#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print( main2(fp))




