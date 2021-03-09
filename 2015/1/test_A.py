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
        seq.append(list(line))

    assert len(seq) == 1

    return seq[0]


def main(fp):
    line = parse(fp)

    return sum( 1 if c == '(' else -1 for c in line)

def main2(fp):
    line = parse(fp)

    s = 0
    for idx,c in enumerate(line):
        s +=  1 if c == '(' else -1
        if s == -1:
            return idx+1


@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 2129920 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))

