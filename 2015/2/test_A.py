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

    p = re.compile( r'^(\d+)x(\d+)x(\d+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append(tuple( int(x) for x in m.groups()))

    return seq


def paper( tup):
    x,y,z = tup
    pairs = [x*y, x*z, y*z]
    return min(pairs) + 2 * sum(pairs)

def ribbon( tup):
    x,y,z = tup
    pairs = [x+y, x+z, y+z]
    return 2 * min(pairs) + x*y*z

def main(fp):
    seq = parse(fp)
    return sum( paper(tup) for tup in seq)

def main2(fp):
    seq = parse(fp)
    return sum( ribbon(tup) for tup in seq)

#@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 58 == main(fp)

#@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 43 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open("data0","rt") as fp:
        assert 34 == main2(fp)

#@pytest.mark.skip
def test_AA1():
    with open("data1","rt") as fp:
        assert 14 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))


