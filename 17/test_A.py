
import io
import pytest

import logging
from logging import debug
import re

def parse(fp,dims):
    alive = set()
    for (y,line) in enumerate(fp):
        line = line.rstrip('\n')
        for x,c in enumerate(line):
            if c == '#':
                cell = [x,y]
                cell.extend( [0]*(dims-2))
                alive.add( tuple(cell))

    return alive

from itertools import product

def count_neighbors( cell, alive, dims):
    count = 0
    for delta in product( *([[-1,0,1]]*dims)):
        if all( x == 0 for x in delta): continue
        adj = tuple( [x+d for (x,d) in zip(cell,delta)])
        if adj in alive:
            count += 1
    return count

def gen_adjacent(alive,dims):
    adjacent = set()
    for cell in alive:
        for delta in product( *([[-1,0,1]]*dims)):
            adj = tuple( [x+d for (x,d) in zip(cell,delta)])
            adjacent.add( adj)

    return adjacent.difference(alive)
                        

def step( current,dims):
    next = set()

    for cell in current:
        if count_neighbors( cell, current, dims) in [2,3]:
            next.add(cell)

    for cell in gen_adjacent(current,dims):
        if count_neighbors( cell, current, dims) in [3]:
            next.add(cell)

    return next

def main( fp, dims=3):
    alive = parse(fp,dims)

    for _ in range(6):
        alive = step(alive,dims)

    return len(alive)


def test_A():
    with open( "data0", "rt") as fp:
        assert 112 == main(fp)
    with open( "data0", "rt") as fp:
        assert 848 == main(fp,4)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main(fp,4))
