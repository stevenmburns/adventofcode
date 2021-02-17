import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p = re.compile( r'^(\S+)\)(\S+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( m.groups())

    return seq


def main(fp):
    seq = parse(fp)
    tbl = {}
    f = defaultdict(list)
    for u,v in seq:
        if u not in tbl:
            tbl[u] = len(tbl)
        if v not in tbl:
            tbl[v] = len(tbl)
        f[tbl[u]].append( tbl[v])

    def ss(i):
        reach = set()
        def dfs(i):
            nonlocal reach
            reach.add(i)
            for j in f[i]:
                if j not in reach:
                    dfs(j)
        dfs(i)
        return reach
                
    s = 0
    for i in range(len(tbl)):
        s += len(ss(i)) - 1

    return s
 
def main2(fp):
    seq = parse(fp)
    tbl = {}
    b = defaultdict(list)
    for u,v in seq:
        if u not in tbl:
            tbl[u] = len(tbl)
        if v not in tbl:
            tbl[v] = len(tbl)
        b[tbl[v]].append( tbl[u])

    # Make sure this is a tree
    for k,v in b.items():
        assert len(v) <= 1

    def ss_b(j):
        edges = set()
        while b[j]:
            i = b[j][0]
            edges.add( (i,j))
            j = i
        return edges
                
    edges_to_SAN = ss_b( tbl['SAN'])
    edges_to_YOU = ss_b( tbl['YOU'])

    d = edges_to_SAN.symmetric_difference(edges_to_YOU)
    #print(p,q,d)

    return len(d)-2

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA():
    with open("data0","rt") as fp:
        assert 4 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))



