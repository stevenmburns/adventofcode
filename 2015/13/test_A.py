import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import json

import sys

logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p = re.compile( r'^(\S+) would (gain|lose) (\d+) happiness units by sitting next to (\S+)\.$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line
        cost = int(m.groups()[2])
        if m.groups()[1] == 'lose':
            cost = -cost
        seq.append( (m.groups()[0], m.groups()[3], cost))

    return seq

def main(fp,*,part2=False):
    seq = parse(fp)
    print(seq)

    
    if part2:
        name_set = set()
        for u, v, c in seq:
            name_set.add(u)
            name_set.add(v)

        assert 'Myself' not in name_set

        for name in name_set:
            seq.append( (name, 'Myself', 0))
            seq.append( ('Myself', name, 0))

    cost_tbl = {}
    for u, v, c in seq:
        if u not in cost_tbl:
            cost_tbl[u] = {}
        cost_tbl[u][v] = c

    names = list(cost_tbl.keys())

    best = None
    for perm in itertools.permutations( names[1:]):
        s = cost_tbl[names[0]][perm[0]] + cost_tbl[perm[-1]][names[0]] + \
            cost_tbl[perm[0]][names[0]] + cost_tbl[names[0]][perm[-1]]
        for i in range(1,len(perm)):
            u,v = perm[i-1],perm[i]
            s += cost_tbl[u][v] + cost_tbl[v][u]
        if best is None or s > best: best = s

    return best

#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 330 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main(fp,part2=True))
