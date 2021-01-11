import pytest
import io
import re

def parse(fp):

    p = re.compile(r'^([.#0-9]+)\s*$')
    seq = []

    tbl = {}

    row = 0
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        if m:

            new_line = ''
            for col, c in enumerate(line):
                if c in "0123456789":
                    tbl[int(c)] = (row,col)
                    new_line += '.'
                else:
                    new_line += c
            seq.append( new_line)
            row += 1
            continue
        assert False, f'"{line}"'

    return seq, tbl

def main(fp):
    seq,tbl = parse(fp)
    print(seq, tbl)

    nrows = len(seq)
    ncols = len(seq[0])

    m = None
    M = None
    tbl2 = {}
    for (k,v) in tbl.items():
        if m is None or k < m: m = k
        if M is None or k > M: M = k
        tbl2[v] = k

    print( nrows, ncols, m, M)

    assert M-m+1 == len(tbl.items())

    all_captured = frozenset( range(m,M+1))

    initial_state = tbl[0], frozenset({0})

    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    def gen_next_states( state):
        (irow,icol), captured = state
        for (drow,dcol) in dirs:
            jrow,jcol = irow+drow,icol+dcol
            if 0 <= jrow < nrows and 0 <= jcol < ncols:
                if seq[jrow][jcol] == '.':
                    if (jrow,jcol) in tbl2:
                        new_captured = set(captured)
                        new_captured.add(tbl2[(jrow,jcol)])
                        next_state = (jrow,jcol), frozenset(new_captured)
                    else:
                        next_state = (jrow,jcol), captured
                    yield next_state
            

    frontier = set( [initial_state])
    reached = set()
    path_length = 0
    while frontier:
        reached = reached.union(frontier)
        new_frontier = set()
        for state in frontier:
            for next_state in gen_next_states(state):
                if next_state[1] == all_captured:
                    return path_length + 1
                new_frontier.add(next_state)
        path_length += 1
        frontier = new_frontier.difference(reached)
        reached = reached.union(frontier)
        print( f'frontier: {len(frontier)} reached: {len(reached)}')
        
    assert False

def main2(fp):
    seq,tbl = parse(fp)
    print(seq, tbl)

    nrows = len(seq)
    ncols = len(seq[0])

    m = None
    M = None
    tbl2 = {}
    for (k,v) in tbl.items():
        if m is None or k < m: m = k
        if M is None or k > M: M = k
        tbl2[v] = k

    print( nrows, ncols, m, M)

    assert M-m+1 == len(tbl.items())

    all_captured = frozenset( range(m,M+1))

    initial_state = tbl[0], frozenset({0}), False

    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    def gen_next_states( state):
        (irow,icol), captured, found0 = state
        for (drow,dcol) in dirs:
            jrow,jcol = irow+drow,icol+dcol
            if 0 <= jrow < nrows and 0 <= jcol < ncols:
                if seq[jrow][jcol] == '.':
                    new_found0 = found0
                    if (jrow,jcol) in tbl2:
                        k = tbl2[(jrow,jcol)]
                        new_captured = set(captured)
                        if captured == all_captured:
                            if k == 0:
                                new_found0 = True
                        else:
                            new_captured.add(k)
                        next_state = (jrow,jcol), frozenset(new_captured), new_found0
                    else:
                        next_state = (jrow,jcol), captured, new_found0
                    yield next_state
            

    frontier = set( [initial_state])
    reached = set()
    path_length = 0
    while frontier:
        reached = reached.union(frontier)
        new_frontier = set()
        for state in frontier:
            for next_state in gen_next_states(state):
                if next_state[2]:
                    return path_length + 1
                new_frontier.add(next_state)
        path_length += 1
        frontier = new_frontier.difference(reached)
        reached = reached.union(frontier)
        print( f'frontier: {len(frontier)} reached: {len(reached)}')
        
    assert False

def test_A():
    with open('data0', 'rt') as fp:
        assert 14 == main(fp)

@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))

