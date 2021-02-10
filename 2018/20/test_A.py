import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

import sys
print(sys.getrecursionlimit())    
sys.setrecursionlimit(100000)

"""
3434 NE Alameda
"""


def toStr( r):
    if type(r) == tuple:
        if r[0] == '|':
            return '(' + '|'.join( toStr(s) for s in r[1]) + ')'
        elif r[0] == '*':
            return ''.join( toStr(s) for s in r[1])
        else:
            assert False, r
    else:
        return r



def parse(fp):
    
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)

    assert len(seq) == 1

    print(line)

    line = seq[0]
    cursor = 0

    """
E -> T
E -> T '|' E
T -> P
T -> P T
P -> 'N' | 'S' | 'E' | 'W'
P -> '(' E ')'

"""


    def primary():
        nonlocal cursor
        c = line[cursor]
        if c in "NEWS":
            cursor += 1
            return c
        elif c == '(':
            cursor += 1
            result = expr()
            c = line[cursor]
            assert c == ')'
            cursor += 1
            return result
        else:
            assert False, (c, cursor)
            
    def term():
        nonlocal cursor
        result = []
        while 0 <= cursor < len(line):
            c = line[cursor]            
            if c in ')|$':
                break
            result.append( primary())

        if len(result) == 1:
            return result[0]
        else:
            return ('*',result)
                
    def expr():
        nonlocal cursor
        result = []

        while 0 <= cursor < len(line):
            result.append( term())
            c = line[cursor]            
            if c == '|':
                cursor += 1
            else:
                break
        if len(result) == 1:
            return result[0]
        else:
            return ('|',result)

    def root():
        nonlocal cursor
        c = line[cursor]            
        assert c == '^'
        cursor += 1
        result = expr()
        c = line[cursor]            
        assert c == '$'
        cursor += 1
        assert cursor == len(line)
        return result


    r = root()

    assert '^' + toStr(r) + '$' == line

    return r

def find_edges( r):

    reachable_edges = set()

    d = { 'N': (-1,0), 'S': (1,0), 'W': (0,-1), 'E': (0,1)}

    def visit( p, r):
        logging.info( f'Calling visit: {p} {toStr(r)}')
        nonlocal reachable_edges
        if type(r) == tuple:
            cmd, lst = r
            if   cmd == '|':

                for idx,s in enumerate(lst):
                    l = list( visit(p,s))
                    ss = set( l)
                    assert len(ss) == len(l)
                    #assert len(ss) == 1
                    #logging.info( f'| len {len(ss)} {ss}')
                    yield from ss
            elif cmd == '*':
                if lst:
                    for pp in visit( p, lst[0]):
                        l = list(visit( pp, (cmd, lst[1:])))
                        ss = set(l)
                        #assert len(ss) == len(l)
                        #assert len(ss) == 1
                        #logging.info( f'* len {len(ss)} {ss}')
                        yield from ss
                else:
                    yield p
        else:
            irow, icol = p
            drow, dcol = d[r]
            pp = irow+drow, icol+dcol

            edge = frozenset([p,pp])
            if edge not in reachable_edges:
                reachable_edges.add(edge)

            yield pp

    # Run the generator
    for p in visit( (0,0), r):
        print( p)
    
    nodes = { n for s in reachable_edges for n in s}

    return nodes, reachable_edges

def print_board( nodes, reachable_edges):
    min_row = min( p[0] for p in nodes)
    max_row = max( p[0] for p in nodes)
    min_col = min( p[1] for p in nodes)
    max_col = max( p[1] for p in nodes)

    for irow in range(min_row,max_row+1):
        line = ''
        for icol in range(min_col,max_col+1):
            p = (irow,icol)
            line += ('.' if p in nodes else ' ') if p != (0,0) else 'X'
            if icol == max_col: continue
            edge = frozenset( [(irow,icol), (irow,icol+1)])
            line += '-' if edge in reachable_edges else ' '
        print(line)
        if irow == max_row: continue
        line = ''
        for icol in range(min_col,max_col+1):
            if icol > min_col:
                line += ' '
            p = (irow,icol)
            edge = frozenset( [(irow,icol), (irow+1,icol)])
            line += '|' if edge in reachable_edges else ' '
        print(line)

def shortest_paths( nodes, reachable_edges):
    
    adjacent_nodes = defaultdict(list)
    for edge in reachable_edges:
        u, v = tuple(edge)
        adjacent_nodes[u].append(v)
        adjacent_nodes[v].append(u)

    frontier = { (0,0)}
    reached = set()
    
    steps = 0
    while True:
        new_frontier = set()
        for u in frontier:
            for v in adjacent_nodes[u]:
                new_frontier.add(v)
        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)
        if not frontier:
            break
        steps += 1
            
    return steps


def main(fp):
    root = parse(fp)
    nodes, reachable_edges = find_edges( root)
    print_board( nodes, reachable_edges)
    length_of_longest_shortest_path = shortest_paths( nodes, reachable_edges)
    return length_of_longest_shortest_path

#@pytest.mark.skip
def test_ex1():
    with open("ex1","rt") as fp:
        assert 3 == main(fp)

#@pytest.mark.skip
def test_ex2():
    with open("ex2","rt") as fp:
        assert 10 == main(fp)

#@pytest.mark.skip
def test_ex3():
    with open("ex3","rt") as fp:
        assert 18 == main(fp)

#@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 10 == main(fp)

#@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 18 == main(fp)

#@pytest.mark.skip
def test_big1():
    with open("big1","rt") as fp:
        assert 23 == main(fp)

#@pytest.mark.skip
def test_big2():
    with open("big2","rt") as fp:
        assert 31 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))


