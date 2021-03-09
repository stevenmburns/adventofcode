import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO)

def parse(fp):

    p = re.compile(r'^(\S+) to (\S+) = (\d+)$')

    seq = []
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( (m.groups()[0],m.groups()[1],int(m.groups()[2])))

    return seq

def main(fp):
    seq = parse(fp)

    cost = {}
    for (u,v,c) in seq:
        if u not in cost:
            cost[u] = {}
        if v not in cost:
            cost[v] = {}
        cost[u][v] = c
        cost[v][u] = c
            
    names = list(cost.keys())

    best_sum = None
    for perm in itertools.permutations(names):
        s = 0
        for i in range(1,len(perm)):
            s += cost[perm[i-1]][perm[i]]
        if best_sum is None or s < best_sum: best_sum = s

    return best_sum

def main2(fp):
    seq = parse(fp)

    cost = {}
    for (u,v,c) in seq:
        if u not in cost:
            cost[u] = {}
        if v not in cost:
            cost[v] = {}
        cost[u][v] = c
        cost[v][u] = c
            
    names = list(cost.keys())

    best_sum = None
    for perm in itertools.permutations(names):
        s = 0
        for i in range(1,len(perm)):
            s += cost[perm[i-1]][perm[i]]
        if best_sum is None or s > best_sum: best_sum = s

    return best_sum

#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 605 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open("data0", "rt") as fp:
        assert 982 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))
