import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    p_leaf = re.compile(r'^(\S+) \((\d+)\)$')
    p_nonleaf = re.compile(r'^(\S+) \((\d+)\) -> (.*)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p_leaf.match(line)
        if m:
            seq.append( ( m.groups()[0], int(m.groups()[1]), []))
            continue
        m = p_nonleaf.match(line)
        if m:
            seq.append( ( m.groups()[0], int(m.groups()[1]), m.groups()[2].split(', ')))
            continue
        assert False, line

    return seq

def main(fp):
    seq = parse(fp)

    amounts = {}

    prev = {}
    for (u,amount,vs) in seq:
        prev[u] = []


    for (u,amount,vs) in seq:
        amounts[u] = amount
        for v in vs:
            prev[v].append(u)

    visited = set()
    order = deque()
    def dfs( u):
        visited.add(u)
        for v in prev[u]:
            if v not in visited:
                dfs(v)
        order.appendleft( u)

    for u in prev.keys():
        if u not in visited:
            dfs(u)

    return order[-1]

def main2(fp):
    seq = parse(fp)

    amounts = {}

    next = {}
    prev = {}
    for (u,amount,vs) in seq:
        prev[u] = []


    for (u,amount,vs) in seq:
        amounts[u] = amount
        next[u] = vs
        for v in vs:
            prev[v].append(u)

    visited = set()
    order = deque()
    def dfs( u):
        visited.add(u)
        for v in prev[u]:
            if v not in visited:
                dfs(v)
        order.appendleft( u)

    for u in prev.keys():
        if u not in visited:
            dfs(u)

    sums = {}
    for u in order:
        histo = {}
        for v in next[u]:
            if sums[v] not in histo:
                histo[sums[v]] = []
            histo[sums[v]].append( v)

        if len(histo.items()) > 2:
            assert False, (u,histo)
        elif len(histo.items()) == 2:
            (k0, v0), (k1, v1) = tuple(histo.items())
            assert len(v0) > len(v1) or len(v1) > len(v0)
            if len(v0) > len(v1):
                assert len(v1) == 1
                # Fix v1
                # what to add to k1 to make it k0
                delta = k0 - k1
                print( v1, delta, amounts[v1[0]])
                return amounts[v1[0]] + delta
            else:
                assert len(v0) == 1
                # Fix v0
                # what to add to k0 to make it k1
                delta = k1 - k0
                print( v0, delta, amounts[v0[0]])
                return amounts[v0[0]] + delta

        sum = 0
        for v in next[u]:
            sum += sums[v]
        sums[u] = sum + amounts[u]

    return None


@pytest.mark.skip
def test_A():
    with open("data0", "rt") as fp:
        assert 'tknk' == main(fp)

@pytest.mark.skip
def test_AA():
    with open("data0", "rt") as fp:
        assert 'tknk' == main2(fp)

@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))


