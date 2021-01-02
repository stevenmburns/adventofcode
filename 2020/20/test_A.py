
import io
import pytest

import logging
from logging import debug
import re

import re
import collections

class Board:
    def __init__(self, m):
        self.m = m

    @property    
    def nrows(self):
        return len(self.m)

    @property    
    def ncols(self):
        return len(self.m[0])

    def __repr__(self):
        result = ''
        for row in self.m:
            result = result + ''.join('#' if x else '.' for x in row) + '\n'
        return result

    def edge(self,ed):
        # top to down
        if ed == 'e':
            return [ row[-1] for row in self.m]
        elif ed == 'w':
            return [ row[ 0] for row in self.m]
        # left to right
        elif ed == 'n':
            return self.m[ 0]
        elif ed == 's':
            return self.m[-1]
        else:
            assert False, ed

    def rot90(self):
        new_m = [ [False]*self.nrows for _ in range(self.ncols)]
        #
        # abc    cf
        # def => be 
        #        ad
        #
        for irow in range(self.nrows):
            for icol in range(self.ncols):
                new_irow = self.ncols-1-icol
                new_icol = irow
                new_m[new_irow][new_icol] = self.m[irow][icol]
        return Board(new_m)

    def mirrory(self):
        new_m = [ [x for x in reversed(row)] for row in self.m]
        return Board(new_m)

    def dihedral(self, idx):
        if idx//4 == 1:
            tmp = Board(self.mirrory().m)
        else:
            tmp = self

        for _ in range(idx%4):
            tmp = tmp.rot90()

        return tmp


def parse(fp):
    tbl = {}

    p_blank = re.compile(r"^$")
    p_row = re.compile(r"^([.#]+)$")
    p_tag = re.compile(r"^Tile (\d+):$")

    tag = None
    current = None
    for line in fp:
        line = line.rstrip('\n')
        m = p_blank.match(line)
        if m:
            tbl[tag] = current
            tag = None
            current = None
            continue
        m = p_tag.match(line)
        if m:
            tag = int(m.groups()[0])
            current = []
            continue
        m = p_row.match(line)
        if m:
            current.append( [ x == '#' for x in m.groups()[0]])
            continue

    assert tag is None and current is None

    new_tbl = {}
    for (k,v) in tbl.items():
        new_tbl[k] = Board(v)
    return new_tbl

def main( fp):
    tbl = parse(fp)

    signatures = {}

    for (k,v) in tbl.items():
        for d in range(8):
            new_board = v.dihedral(d)
            for e in ['e','w','n','s']:
                ed = new_board.edge(e)
                triple = (k, d, e)
                sig = ''.join( '#' if x else '.' for x in ed)
                if sig not in signatures:
                    signatures[sig] = []
                signatures[sig].append( triple)

    non_matching = {}
    matching = {}

    for (k,v) in signatures.items():
        assert len(v) in [4,8]
        if len(v) == 4:
            for x in v:
                if x[0] not in non_matching:
                    non_matching[x[0]] = []
                non_matching[x[0]].append( (x[1],x[2]))
    prod = 1
    for (k,v) in non_matching.items():
        assert len(v) in [8,16]
        if len(v) == 16:
            prod *= k
        
    return prod

def main2( fp):
    tbl = parse(fp)

    signatures = {}

    for (k,v) in tbl.items():
        for d in range(8):
            new_board = v.dihedral(d)
            for e in ['e','w','n','s']:
                ed = new_board.edge(e)
                triple = (k, d, e)
                sig = ''.join( '#' if x else '.' for x in ed)
                if sig not in signatures:
                    signatures[sig] = []
                signatures[sig].append( triple)

    non_matching = {}

    for (k,v) in signatures.items():
        assert len(v) in [4,8]
        if len(v) == 4:
            for x in v:
                if x[0] not in non_matching:
                    non_matching[x[0]] = []
                non_matching[x[0]].append( (x[1],x[2]))

    corners = {}
    edges = {}
    for (k,v) in non_matching.items():
        assert len(v) in [8,16]
        if len(v) == 16:
            corners[k] = v
        if len(v) == 8:
            edges[k] = v


    # upper left
    t = {}
    for e in ['w','n']:
        t[e] = []
        for (k,v) in list(corners.items())[:1]:
            for vv in v:
                if vv[1] == e:
                    t[e].append( (k,vv[0]))

    stitch = {}
    stitch[(0,0)] = list(set(t['w']).intersection(set(t['n'])))[0]

    def find_set( irow, icol, drow, dcol, e0, e1):
        id, d = stitch[(irow-drow,icol-dcol)]
        ed = tbl[id].dihedral(d).edge(e0)
        sig = ''.join( '#' if x else '.' for x in ed)
        matches = set()
        for v in signatures[sig]:
            if v[0] != id and v[2] == e1:
                matches.add( (v[0],v[1]))
        return matches
    def get_singleton(s):
        assert len(s) == 1
        return list(s)[0]

    # assume square shape
    assert len(edges) % 4 == 0
    N = len(edges)//4 + 2
    for irow in range(1,N):
        stitch[(irow,0)] = get_singleton(find_set(irow, 0, 1, 0, 's', 'n'))

    for icol in range(1,N):
        stitch[(0,icol)] = get_singleton(find_set(0, icol, 0, 1, 'e', 'w'))

    for irow in range(1,N):
        for icol in range(1,N):
            s0 = find_set(irow,icol,0,1,'e','w')
            s1 = find_set(irow,icol,1,0,'s','n')
            stitch[(irow,icol)] = get_singleton(s0.intersection(s1))
    
    master_id, master_d = stitch[(0,0)]
    master = tbl[master_id].dihedral(master_d)

    m = [ [False]*((master.ncols-2)*N) for _ in range((master.nrows-2)*N)]
    for irow in range(0,N):
        for icol in range(0,N):
            c_id, c_d = stitch[(irow,icol)]
            c = tbl[c_id].dihedral(c_d)
            for jrow in range(1,c.nrows-1):
                for jcol in range(1,c.ncols-1):
                    m[irow*(c.nrows-2)+jrow-1][icol*(c.ncols-2)+jcol-1] = c.m[jrow][jcol]

    big_board = Board(m)

    ship_txt = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
    m_ship = [ [x == '#' for x in row] for row in ship_txt.split('\n')]
    assert len(m_ship) == 3 and len(m_ship[0]) == len(m_ship[1]) == len(m_ship[2])

    ship_board = Board(m_ship)

    matches = set()

    
    for d in range(8):
        flipped_ship_board = ship_board.dihedral(d)
        for irow in range(big_board.nrows-flipped_ship_board.nrows+1):
            for icol in range(big_board.ncols-flipped_ship_board.ncols+1):
                match = True
                for jrow in range(flipped_ship_board.nrows):
                    for jcol in range(flipped_ship_board.ncols):
                        if flipped_ship_board.m[jrow][jcol]:
                            if not big_board.m[irow+jrow][icol+jcol]:
                                match = False
                if match:
                    for jrow in range(flipped_ship_board.nrows):
                        for jcol in range(flipped_ship_board.ncols):
                            if flipped_ship_board.m[jrow][jcol]:
                                if big_board.m[irow+jrow][icol+jcol]:
                                    matches.add( (irow+jrow, icol+jcol))

    s = 0
    for row in big_board.m:
        s += sum(1 for x in row if x)

    return s - len(matches)

def test_rot90():
    m = [[True,True],
         [True,False],
         [True,False]]
 
    new_m = Board(m).dihedral(1)

    assert [[True,False,False],
            [True,True,True]] == new_m.m

def test_rot180():
    m = [[True,True],
         [True,False],
         [True,False]]

    new_m = Board(m).dihedral(2)

    assert [[False,True],
            [False,True],
            [True,True]] == new_m.m

def test_rot270():
    m = [[True,True],
         [True,False],
         [True,False]]
 
    new_m = Board(m).dihedral(3)

    assert [[True,True,True],
            [False,False,True]] == new_m.m

def test_mirrory():
    m = [[True,True],
         [True,False],
         [True,False]]
 
    new_m = Board(m).dihedral(4)

    assert [[True,True],
            [False,True],
            [False,True]] == new_m.m

def test_mirrorx():
    m = [[True,True],
         [True,False],
         [True,False]]
 
    new_m = Board(m).dihedral(6)

    assert [[True,False],
            [True,False],
            [True,True]] == new_m.m

def test_mirrord():
    m = [[True,True],
         [True,False],
         [True,False]]
 
    new_m = Board(m).dihedral(5)

    assert [[True,True,True],
            [True,False,False]] == new_m.m

def test_mirrora():
    m = [[True,True],
         [True,False],
         [True,False]]
 
    new_m = Board(m).dihedral(7)

    assert [[False,False,True],
            [True,True,True]] == new_m.m


def test_A():
    with open( "data0", "rt") as fp:
        assert 20899048083289 == main(fp)

def test_A2():
    with open( "data0", "rt") as fp:
        assert 273 == main2(fp)

def test_C():
    with open( "data", "rt") as fp:
        assert 17250897231301 == main(fp)

def test_C2():
    with open( "data", "rt") as fp:
        assert 1576 == main2(fp)
