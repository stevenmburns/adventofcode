
import io
import pytest

import logging
from logging import debug
import re

from collections import deque


#logging.basicConfig(level=logging.DEBUG)

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(int(line))
    return seq



def main( fp):
    seq = parse(fp)

    seq.sort()

    q = deque(seq)
    q.appendleft(0)
    q.append(seq[-1]+3)
    seq = list(q)

    diffs = [ seq[i+1] - seq[i] for i in range(len(seq)-1)]

    ones = sum([ 1 for d in diffs if d == 1])
    threes = sum([ 1 for d in diffs if d == 3])
    others = sum([ 1 for d in diffs if d not in [1,3]])

    assert others == 0

    return ones * threes


def main2(fp):
    seq = parse(fp)

    seq.sort()

    q = deque(seq)
    q.appendleft(0)
    q.append(seq[-1]+3)
    seq = list(q)

    diffs = [ seq[i+1] - seq[i] for i in range(len(seq)-1)]

    lol = []
    current_lst = [seq[0]]
    for i in range(1,len(seq)):
        if seq[i] - seq[i-1] == 3:
            lol.append(current_lst)
            current_lst = [seq[i]]
        else:
            current_lst.append(seq[i])
    lol.append(current_lst)

    histo = {}
    for x in lol:
        n = len(x)
        if n not in histo:
            histo[n] = 0
        histo[n] += 1
    print(sorted(histo.items()))

    tbl = { 1: 1, 2: 1, 3: 2, 4: 4, 5: 7}

    result = 1
    for (k,v) in histo.items():
        for i in range(v):
            result *= tbl[k]

    return result

def test_A():
    with open( "data0", "rt") as fp:
        assert 35 == main(fp)

    with open( "data0", "rt") as fp:
        assert 8 == main2(fp)

def test_B():
    with open( "data1", "rt") as fp:
        assert 220 == main(fp)

    with open( "data1", "rt") as fp:
        assert 19208 == main2(fp)



def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))

    with open( "data", "rt") as fp:
        print(main2(fp))
