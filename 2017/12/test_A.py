import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append( line.split(','))
    assert len(seq) == 1
    return seq[0]


dirs = { 'n': (-1,2), 'ne': (0,1), 'nw': (-1,1),
         's': (1,-2), 'se': (1,-1), 'sw': (0,-1)}


def distance( p):
    (x,y) = p
    

    """
    n,ne basis:
    x = -a
    y =  2a + b
=>
    a = -x
    b = y + 2x
"""
    """
    n,nw basis:
    x = -a + -b
    y = 2a +  b
=>
    a = x + y
    b = -2*x - y
"""
    """
    ne,nw basis:
    x =  -b
    y = a + b
=>
    b = -x
    a = x + y 
"""

    
    tup = abs(-x)+abs(2*x+y), abs(x+y)+abs(-2*x-y), abs(-x)+abs(x+y)

    return min( *tup)


def sim(seq):
    (x,y) = (0,0)

    for dir in seq:
        (dx,dy) = dirs[dir]
        x,y = x+dx,y+dy
            
    if False:
        reached = set()
        frontier = {(x,y)}
        if (x,y) == (0,0):
            return 0
        path_length = 0
        while len(frontier) > 0:
            new_frontier = set()
            for (x,y) in frontier:
                for _,(dx,dy) in dirs.items():
                    xx,yy = x+dx,y+dy
                    new_frontier.add( (xx,yy))
            path_length += 1
            for (x,y) in new_frontier:
                if (x,y) == (0,0):
                    return path_length
            reached = reached.union(frontier)
            frontier = new_frontier.difference(reached)
            #print( len(reached), len(frontier))

    return distance( (x,y))

def sim2(seq):
    (x,y) = (0,0)

    M = None
    for dir in seq:
        (dx,dy) = dirs[dir]
        x,y = x+dx,y+dy
        d = distance( (x,y))
        if M is None or M<d: M = d
            
    if False:
        reached = set()
        frontier = {(x,y)}
        if (x,y) == (0,0):
            return 0
        path_length = 0
        while len(frontier) > 0:
            new_frontier = set()
            for (x,y) in frontier:
                for _,(dx,dy) in dirs.items():
                    xx,yy = x+dx,y+dy
                    new_frontier.add( (xx,yy))
            path_length += 1
            for (x,y) in new_frontier:
                if (x,y) == (0,0):
                    return path_length
            reached = reached.union(frontier)
            frontier = new_frontier.difference(reached)
            #print( len(reached), len(frontier))

    return M

def main(fp):
    seq = parse(fp)
    return sim(seq)

def main2(fp):
    seq = parse(fp)
    return sim2(seq)

def test_A0():
    txt = """ne,ne,ne
"""
    with io.StringIO(txt) as fp:
        assert 3 == main(fp)

def test_A1():
    txt = """ne,ne,sw,sw
"""
    with io.StringIO(txt) as fp:
        assert 0 == main(fp)

def test_A2():
    txt = """ne,ne,s,s
"""
    with io.StringIO(txt) as fp:
        assert 2 == main(fp)

def test_A3():
    txt = """se,sw,se,sw,sw
"""
    with io.StringIO(txt) as fp:
        assert 3 == main(fp)

def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))


