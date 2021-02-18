import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import math

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( line)

    return seq

def compute_best( s):
    result = []
    for p in s:
        ratios = defaultdict(list)
        for q in s:
            if p == q: continue
            drow, dcol = q[0]-p[0], q[1]-p[1]
            f = abs(math.gcd(drow,dcol))
            ratios[ (drow//f,dcol//f)].append( q)
        result.append( (len(ratios), p))
        
    result.sort()

    return result[-1]


def main(fp):
    seq = parse(fp)

    s = set()
    for irow, line in enumerate(seq):
        for icol, c in enumerate(line):
            if c == '#':
                s.add( (irow,icol))

    return compute_best(s)[0]

def toDegrees( d):
    q = math.atan2( d[0], d[1]) * 180.0 / math.pi + 90
    if q < 0:
        q += 360
    return q

def main2(fp):
    seq = parse(fp)

    s = set()
    for irow, line in enumerate(seq):
        for icol, c in enumerate(line):
            if c == '#':
                s.add( (irow,icol))

    p = compute_best(s)[1]
    print(f'p {p}')

    ratios = defaultdict(list)
    for q in s:
        if p == q: continue
        drow, dcol = q[0]-p[0], q[1]-p[1]
        f = abs(math.gcd(drow,dcol))
        ratios[ (drow//f,dcol//f)].append( q)

    def distsq(q):
        return -((q[0]-p[0])**2 + (q[1]-p[1])**2)

    for k in ratios.keys():
        ratios[k].sort(key=distsq)

    order = []
    for ratio in ratios.keys():
        order.append( (toDegrees(ratio), ratio))

    order.sort()

    count = 0
    while True:
        for theta, ratio in order:
            if ratios[ratio]:
                top = ratios[ratio].pop()
                count += 1
                print( f'count {count} theta {theta} top {top}')
                if count == 200:
                    return 100*top[1] + top[0]

def test_toDegrees():
    assert abs( toDegrees( (-1,0))) < 0.001
    assert abs( toDegrees( (0,1)) - 90) < 0.001
    assert abs( toDegrees( (1,0)) - 180) < 0.001
    assert abs( toDegrees( (0,-1)) - 270) < 0.001


@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 8 == main(fp)

@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 33 == main(fp)

@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        assert 35 == main(fp)

@pytest.mark.skip
def test_A3():
    with open("data3","rt") as fp:
        assert 41 == main(fp)

@pytest.mark.skip
def test_A4():
    with open("data4","rt") as fp:
        assert 210 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

@pytest.mark.skip
def test_AA4():
    with open("data4","rt") as fp:
        assert 802 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))




