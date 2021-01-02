
import io
import pytest

import logging
from logging import debug
import re

import re
import collections
from collections import deque

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        s = []
        i = 0
        while i < len(line):
            if line[i] in ['s','n']:
                s.append( line[i] + line[i+1])
                i += 2
            else:
                s.append( line[i])
                i += 1
        seq.append(s)

    return seq

def move( dir, p):
    x,y = p
    if dir == 'ne':
        y += 1
    elif dir == 'nw':
        x -= 1
        y += 1
    elif dir == 'se':
        x += 1
        y -= 1
    elif dir == 'sw':
        y -= 1
    elif dir == 'w':
        x -= 1
    elif dir == 'e':
        x += 1
    return (x,y)

def pos( s):
    p = 0,0
    for dir in s:
        p = move( dir, p)
    return p

def sim(seq):
    tiles = {}

    for s in seq:
        p = pos(s)
        if p in tiles:
            if tiles[p] == 'black':
                tiles[p] = 'white'
            elif tiles[p] == 'white':
                tiles[p] = 'black'
            else:
                assert False, tiles[p]
        else:
            tiles[p] = 'black'

    return tiles


def neighbors( black, p):
    count = 0
    for dir in ['nw','ne','sw','se','w','e']:
        p0 = move(dir,p)
        if p0 in black:
            count += 1
    return count

def step(tbl):
    black = { k for (k,v) in tbl.items() if v == 'black'}
    adjacent = set()
    for p in black:
        for dir in ['nw','ne','sw','se','w','e']:
            p0 = move(dir,p)
            adjacent.add(p0)

    adjacent_white = adjacent.difference(black)

    for p in black:
        n = neighbors(black, p)
        if n == 0 or n > 2:
            tbl[p] = 'white'

    for p in adjacent_white:
        n = neighbors(black, p)
        if n == 2:
            tbl[p] = 'black'

    
def steps(tbl,nsteps):
    for _ in range(nsteps):
        step(tbl)
    count = 0
    for (k,v) in tbl.items():
        if v == 'black':
            count += 1
    return count

def main( fp):
    seq = parse(fp)
    tbl = sim(seq)
    count = 0
    for (k,v) in tbl.items():
        if v == 'black':
            count += 1
    return count

def main2( fp):
    seq = parse(fp)
    return steps(sim(seq),nsteps=100)


def test_A():
    with open("data0", "rt") as fp:
        assert 10 == main(fp)
    with open("data0", "rt") as fp:
        assert 2208 == main2(fp)

def test_C():
    with open("data", "rt") as fp:
        print(main(fp))
    with open("data", "rt") as fp:
        print(main2(fp))


