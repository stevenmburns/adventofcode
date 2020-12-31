
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

    def dihederal(self, idx):
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
            new_board = v.dihederal(d)
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
            new_board = v.dihederal(d)
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

    # non_matching 'w' edges, assume square shape
    assert len(edges) % 4 == 0
    for irow in range(1,len(edges)//4+1):
        t = {}
        for e in ['w']:
            t[e] = []
            for (k,v) in list(edges.items()):
                for vv in v:
                    if vv[1] == e:
                        t[e].append( (k,vv[0]))

        id, d = stitch[(irow-1,0)]
        ed = tbl[id].dihederal(d).edge('s')
        sig = ''.join( '#' if x else '.' for x in ed)
        for v in signatures[sig]:
            if v[0] != id and v[2] == 'n':
                stitch[(irow,0)] = v[0], v[1]


    # lower left
    t = {}
    for e in ['w','s']:
        t[e] = []
        for (k,v) in list(corners.items()):
            for vv in v:
                if vv[1] == e:
                    t[e].append( (k,vv[0]))

    id, d = stitch[(len(edges)//4,0)]
    ed = tbl[id].dihederal(d).edge('s')
    sig = ''.join( '#' if x else '.' for x in ed)
    for v in signatures[sig]:
        if v[0] != id and v[2] == 'n':
            stitch[(irow,0)] = v[0], v[1]



    print(set(t['w']).intersection(set(t['s'])))



    print(stitch)
    print(len(corners))
    print(len(edges))

    return 0

def test_rot90():
    m = [[True,False,True],
         [False,True,False]]
 
    new_m = Board(m).rot90()

    assert [[True,False],
            [False,True],
            [True,False]] == new_m.m

def test_rot180():
    m = [[True,False,True],
         [False,True,False]]
 
    new_m = Board(m).dihederal(2)

    assert [[False,True,False],
            [True,False,True]] == new_m.m

def test_rot270():
    m = [[True,False,True],
         [False,True,False]]
 
    new_m = Board(m).dihederal(3)

    assert [[False,True],
            [True,False],
            [False,True]] == new_m.m

def test_mirrorx():
    m = [[True,False,True],
         [False,True,False]]
 
    new_m = Board(m).dihederal(6)

    assert [[False,True,False],
            [True,False,True]] == new_m.m

def test_mirrory():
    m = [[True,True,False],
         [False,True,True]]
 
    new_m = Board(m).mirrory()

    assert [[False,True,True],
            [True,True,False]] == new_m.m


def test_A():
    with open( "data0", "rt") as fp:
        assert 20899048083289 == main(fp)

def test_A2():
    with open( "data0", "rt") as fp:
        assert 0 == main2(fp)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
def test_C2():
    with open( "data", "rt") as fp:
        assert 0 == main2(fp)
