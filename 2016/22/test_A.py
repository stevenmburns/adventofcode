import pytest
import io
import re
import hashlib
from collections import deque

def parse(fp):
    seq = []
    p_other = re.compile(r'^(root|Filesystem).*$')
    p = re.compile(r'^/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)\%$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        if m:
            seq.append( (int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[3]), int(m.groups()[4])))
            continue
        m = p_other.match(line)
        if m:
            continue
        assert False, line

    return seq

def compute_pairs(seq):
    pairs = []
    for (x0,y0,used0,avail0) in seq:
        for (x1,y1,used1,avail1) in seq:
            if (x0,y0) != (x1,y1):
                if used0 > 0 and used0 <= avail1:
                    pairs.append( ((x0,y0),(x1,y1)))
    return len(pairs)


def main(fp):
    seq = parse(fp)
    return compute_pairs(seq)

def main2(fp):
    seq = parse(fp)

    mx, Mx, my, My = None, None, None, None

    tbl = {}

    Mused, mtotal = None,None


    for (x,y,used,avail) in seq:
        total = used+avail
        if mx is None or mx > x: mx = x
        if Mx is None or Mx < x: Mx = x
        if my is None or my > y: my = y
        if My is None or My < y: My = y
        tbl[(y,x)] = (used,avail)
        if total <= 500:
            if Mused is None or Mused < used: Mused = used
            if mtotal is None or mtotal > total: mtotal = total

    print( 'SMB',Mused, mtotal)

    print(mx,Mx,my,My)

    assert mx == 0 and my == 0

    nrows = My+1
    ncols = Mx+1

    board = [ [ False for j in range(ncols)] for i in range(nrows)]

    for (x,y,used,avail) in seq:    
        board[y][x] = used == 0

    zeros = []

    for (irow,row) in enumerate(board):
        def s(irow,icol):
            total = tbl[(irow,icol)][0]+tbl[(irow,icol)][1]
            result = f'{total:3d}'
            if total < tbl[(0,ncols-1)][0]:
                result = '   '
            return result

        def t(irow,icol):
            used,avail = tbl[(irow,icol)]
            result = f'{used:3d}/{used+avail:3d}'
            return result

        def f(irow,icol):
            (used,avail) = tbl[(irow,icol)]
            if used+avail > 500:
                return '#'
            elif used == 0:
                zeros.append( (irow,icol))
                return '_'
            else:
                return '.'

        print( ''.join( f(irow,icol) for (icol,c) in enumerate(row)))

    tbl = {}
    for (x,y,used,avail) in seq:
            tbl[(y,x)] = (used,avail)


    # hack to modify table so get more shared states
    new_tbl = {}
    for (k, (used,avail)) in tbl.items():
        if used+avail >= 500:
            new_used, new_avail = 500, 0
        elif used == 0:
            new_used, new_avail = 0, 100
        else:
            new_used, new_avail = 100, 0
        new_tbl[k] = new_used, new_avail

    tbl = new_tbl

    init_state = (0,ncols-1), tuple( tuple( tbl[(irow,icol)][0] for icol in range(ncols)) for irow in range(nrows))

    totals = [ [ tbl[(irow,icol)][0]+tbl[(irow,icol)][1] for icol in range(ncols)] for irow in range(nrows)]


    def gen_next_states( state):
        target_data,useds = state
        dirs = [ (0,-1), (0,1), (-1,0), (1,0)]
        for irow in range(nrows):
            for icol in range(ncols):
                for drow, dcol in dirs:
                    jrow,jcol = irow+drow,icol+dcol
                    if 0 <= jrow < nrows and 0 <= jcol < ncols:
                        move_amount = useds[irow][icol]
                        if move_amount == 0: continue
                        if totals[jrow][jcol] >= useds[jrow][jcol] + move_amount:

                            new_target_data = (jrow,jcol) if (irow,icol) == target_data else target_data
                            a = [ list(row) for row in useds]
                            a[irow][icol] -= move_amount
                            a[jrow][jcol] += move_amount
                            new_useds = tuple( tuple(row) for row in a)
                            yield new_target_data,new_useds

    frontier = set( [init_state])
    print(frontier)

    reached = set()

    path_length = 0
    
    while frontier:
        reached = reached.union(frontier)
        new_frontier = set()
        for state in frontier:
            for next_state in gen_next_states(state):
                if next_state[0] == (0,0):
                    return path_length + 1
                new_frontier.add(next_state)
        path_length += 1
        frontier = new_frontier.difference(reached)
        counts = []
        histo = {}
        for target,useds in frontier:
            count = 0
            for row in useds:
                for u in row:
                    if u == 0:
                        count += 1
            if count not in histo:
                histo[count] = 0
            histo[count] += 1

                        
        reached = reached.union(frontier)
        print( f'frontier: {len(frontier)} reached: {len(reached)} {histo}')

    assert False

def test_AA():
    with open("data0", "rt") as fp:
        print( main2(fp))

@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print( main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print( main2(fp))
