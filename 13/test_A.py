
import io
import pytest

import logging
from logging import debug
import re

from collections import deque
from copy import deepcopy

#logging.basicConfig(level=logging.DEBUG)

def parse(fp):
    p = re.compile(r'^([NSEWLRF])(\d+)$')

    lines = []
    for line in fp:
        line = line.rstrip('\n')
        lines.append(line)

    assert len(lines) == 2
    start = int(lines[0])
    
    routes = [ None if x == 'x' else int(x) for x in lines[1].split(',')]
    print(routes)


    return start, routes

def main( fp):
    start, routes = parse(fp)

    mn = min( x for x in routes if x is not None)
    mx = max( x for x in routes if x is not None)

    for t in range( start, start+mn):
        for route in routes:
            if route is None: continue
            if t % route == 0:
                print(t, route)
                return route*(t-start)

    print(mn,mx)

    return 0


import math

def lcm2( a, b):
    return a*b // math.gcd(a,b)

def lcm( lst):
    result = 1
    for x in lst:
        result = lcm2( result,x )
    return result

def combine( p0, p):
    v0, m0 = p0
    v, m = p
    l = lcm2(m0,m)
    for i in range(v0,l,m0):
        if (i+v) % m == 0:
            return (i,l)
    assert False 


def compute( indexed_routes):

    p0 = indexed_routes[0]
    for p in indexed_routes[1:]:
        p1 = combine( p0, p)
        print(p0,p,'=>',p1)
        p0 = p1

    return p0[0]
    


def main2( fp):
    start, routes = parse(fp)

    indexed_routes = [ (idx,x) for (idx,x) in enumerate(routes) if x is not None]
    print(indexed_routes)

    return compute(indexed_routes)


def test_lcm():
    assert 12 == lcm( [1,2,3,4])
    assert 36 == lcm( [12,18])


def test_B1():
    assert 754018 == compute( [(0,67),(1,7),(2,59),(3,61)])

def test_B2():
    assert 779210 == compute( [(0,67),(2,7),(3,59),(4,61)])

def test_B3():
    assert 1261476 == compute( [(0,67),(1,7),(3,59),(4,61)])

def test_B4():
    assert 1202161486 == compute( [(0,1789),(1,37),(2,47),(3,1889)])

def test_A():
    with open( "data0", "rt") as fp:
        assert 295 == main(fp)
    with open( "data0", "rt") as fp:
        assert 1068781 == main2(fp)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))

