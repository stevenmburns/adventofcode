import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( [ (x[:1], int(x[1:])) for x in line.split(',')])

    assert len(seq) == 2

    return seq

def find_reachable( wire):
    x,y = 0,0
    reach = set()
    dirs = { 'U': (0,1), 'D': (0,-1), 'L': (-1,0), 'R': (1,0)}
    for dir, dist in wire:
        dx,dy = dirs[dir]
        for _ in range(dist):
            x,y = x+dx, y+dy
            reach.add( (x,y))
    return reach, delays

def dist( p):
    return sum( abs(x) for x in p)

def main(fp):
    w0, w1 = parse(fp)

    reach0 = find_reachable(w0)
    reach1 = find_reachable(w1)

    p = min( reach0.intersection(reach1), key=dist)
    print(p)

    return dist(p)

def find_reachable2( wire):
    dirs = { 'U': (0,1), 'D': (0,-1), 'L': (-1,0), 'R': (1,0)}

    x,y = 0,0
    reach = {}
    delay = 0
    for dir, dist in wire:
        dx,dy = dirs[dir]
        for i in range(dist):
            x,y,delay = x+dx, y+dy,delay+1
            if (x,y) not in reach:
                reach[(x,y)] = delay
    return reach

def main2(fp):
    w0, w1 = parse(fp)

    reach0 = find_reachable2(w0)
    reach1 = find_reachable2(w1)

    def metric( p):
        return reach0[p] + reach1[p]

    p = min( set(reach0.keys()).intersection(set(reach1.keys())), key=metric)
    print(p)

    return metric(p)

@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 6 == main(fp)

@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 159 == main(fp)

@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        assert 135 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open("data0","rt") as fp:
        assert 30 == main2(fp)

#@pytest.mark.skip
def test_AA1():
    with open("data1","rt") as fp:
        assert 610 == main2(fp)

#@pytest.mark.skip
def test_AA2():
    with open("data2","rt") as fp:
        assert 410 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))


