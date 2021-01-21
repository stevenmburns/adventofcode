import sys
import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    p_line = re.compile(r'^([.#/]+) => ([.#/]+)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p_line.match(line)
        assert m, line
        seq.append( m.groups())

    def spl( s):
        lst = s.split('/')
        assert lst
        assert all( len(lst[0]) == len(ss) for ss in lst[1:])
        return tuple(lst)

    new_seq = []
    for (lhs, rhs) in seq:
        new_seq.append( (spl(lhs), spl(rhs)))

    return new_seq

def r0( sboard):
    return sboard

def r90( sboard):
    n = len(sboard)
    assert n == len(sboard[0])

    a = [ [ None for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            a[i][j] = sboard[j][n-1-i]

    return tuple( ''.join( a[i][j] for j in range(n)) for i in range(n))

def r180( sboard):
    return r90( r90( sboard))

def r270( sboard):
    return r90( r90( r90( sboard)))

def mx( sboard):
    n = len(sboard)
    assert n == len(sboard[0])

    a = [ [ None for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            a[i][j] = sboard[n-1-i][j]

    return tuple( ''.join( a[i][j] for j in range(n)) for i in range(n))

def my( sboard):
    return r90( mx( r270( sboard)))

def md( sboard):
    return r270( mx( sboard))

def ma( sboard):
    return r90( mx( sboard))

def test_r90():
    inp = ( '#..',
            '##.',
            '##.')

    out = ( '...',
            '.##',
            '###')

    assert out == r90(inp)

def test_r180():
    inp = ( '#..',
            '##.',
            '##.')

    out = ( '.##',
            '.##',
            '..#')

    assert out == r180(inp)

def test_r270():
    inp = ( '#..',
            '##.',
            '##.')

    out = ( '###',
            '##.',
            '...')

    assert out == r270(inp)

def test_mx():
    inp = ( '#..',
            '##.',
            '##.')

    out = ( '##.',
            '##.',
            '#..')

    assert out == mx(inp)

def test_my():
    inp = ( '#..',
            '##.',
            '##.')

    out = ( '..#',
            '.##',
            '.##')

    assert out == my(inp)

def test_md():
    inp = ( '#..',
            '##.',
            '##.')

    out = ( '###',
            '.##',
            '...')

    assert out == md(inp)

def test_ma():
    inp = ( '#..',
            '##.',
            '##.')

    out = ( '...',
            '##.',
            '###')

    assert out == ma(inp)


def main(fp,nsteps):
    seq = parse(fp)

    dihedral = [r0, r90, r180, r270, mx, my, md, ma]

    tbl = {}
    for (lhs,rhs) in seq:
        for f in dihedral:
            new_lhs = f(lhs)
            if new_lhs not in tbl: tbl[new_lhs] = set()
            tbl[new_lhs].add( rhs)

    def partition_board( board_in, n, k):
        assert n % k == 0
        board = []
        for irow in range(0,n,k):
            row = []
            for icol in range(0,n,k):
                sboard = []
                for jrow in range(k):
                    srow = ''
                    for jcol in range(k):
                        srow += board_in[irow+jrow][icol+jcol]
                    sboard.append( srow)
                row.append( tuple(sboard))
            board.append(row)
        return board

    def flatten_board( board_in):
        m = len(board_in)
        assert m == len(board_in[0])
        k = len(board_in[0][0])
        assert k == len(board_in[0][0][0])
        board = []
        for irow in range(m):
            for jrow in range(k):
                row = ''
                for icol in range(m):
                    for jcol in range(k):
                        row += board_in[irow][icol][jrow][jcol]
                board.append(row)
        return board

    def apply_rules( board_in):
        m = len(board_in)
        assert m == len(board_in[0])

        board = []
        for irow in range(m):
            row = []
            for icol in range(m):
                sboard = board_in[irow][icol]
                if sboard in tbl:
                    s = tbl[sboard]
                    assert len(s) == 1
                    row.append( list(s)[0])
                else:
                    assert False, sboard
            board.append(row)
        return board

    def step(board_in):
        n = len(board_in)
        assert n == len(board_in[0])
        for k in [2,3]:
            if n % k == 0:
                board = partition_board( board_in, n, k)
                new_board = apply_rules(board)
                return flatten_board(new_board)
        assert False, n
            
    def count_live( board):
        count = 0
        for row in board:
            count += sum( 1 for c in row if c == '#')
        return count

    start = ['.#.', '..#', '###']

    board = start
    print(count_live(board))
    for _ in range(nsteps):
        board = step(board)
        print(count_live(board))

    return count_live(board)

#@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 12 == main(fp,2)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp,5))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main(fp,18))


