import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import heapq

logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)

    assert len(seq) == 1

    return seq[0]

def main(fp):
    line = parse(fp)

    dirs = {'<': (0,-1), '>': (0,1), '^': (-1,0), 'v': (1,0)}

    p = 0,0

    reached = set([p])

    for c in line:
        d = dirs[c]
        p = p[0]+d[0],p[1]+d[1]
        reached.add(p)

    return len(reached)

def main2(fp):
    line = parse(fp)

    dirs = {'<': (0,-1), '>': (0,1), '^': (-1,0), 'v': (1,0)}

    p0 = 0,0
    p1 = 0,0

    reached0 = set([p0])
    reached1 = set([p1])

    for idx,c in enumerate(line):
        d = dirs[c]
        if idx % 2 == 0:
            p0 = p0[0]+d[0],p0[1]+d[1]
            reached0.add(p0)
        else:
            p1 = p1[0]+d[0],p1[1]+d[1]
            reached1.add(p1)

    return len(reached0.union(reached1))

@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 2 == main(fp)

@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 4 == main(fp)

@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        assert 2 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open("data3","rt") as fp:
        assert 3 == main2(fp)

#@pytest.mark.skip
def test_AA1():
    with open("data1","rt") as fp:
        assert 3 == main2(fp)

#@pytest.mark.skip
def test_AA2():
    with open("data2","rt") as fp:
        assert 11 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))


