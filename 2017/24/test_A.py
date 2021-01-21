import sys
import pytest
import io
import re
import itertools
from collections import deque


def parse(fp):
    seq = []
    p = re.compile(r'^(\d+)/(\d+)$') 

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        if m:
            seq.append( tuple( int(x) for x in m.groups()))
            if seq[-1][0] > seq[-1][1]:
                seq[-1] = seq[-1][1], seq[-1][0]
            continue
        assert False, line

    return seq

def main(fp):
    seq = parse(fp)
    print(len(seq))
    print(seq)

    tbl = {}
    for tup in seq:
        if tup not in tbl: tbl[tup] = 0
        tbl[tup] += 1

    assert all( v == 1 for k,v in tbl.items())

    remainder = set( seq)
    assert len(remainder) == len(seq)

    # node, remainding edges, cost
    state = 0, frozenset(remainder), 0

    reached = set()
    frontier = { state }

    def rm( fz, obj):
        s = set(fz)
        s.remove(obj)
        return frozenset(s)

    while frontier:
        print( len(frontier))
        new_frontier = set()
        for state in frontier:
            node, remaining_edges, cost = state
            for tup in seq:
                if tup not in remaining_edges: continue
                if tup[0] == node:
                    new_state = tup[1], rm(remaining_edges,tup), cost+tup[0]+tup[1]
                    new_frontier.add(new_state)
                elif tup[1] == node:
                    new_state = tup[0], rm(remaining_edges,tup), cost+tup[0]+tup[1]
                    new_frontier.add(new_state)

        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)


    M = None
    for node, remaining_edges, cost in reached:
        if M is None or M < cost: M = cost

    return M

def main2(fp):
    seq = parse(fp)
    print(len(seq))
    print(seq)

    tbl = {}
    for tup in seq:
        if tup not in tbl: tbl[tup] = 0
        tbl[tup] += 1

    assert all( v == 1 for k,v in tbl.items())

    remainder = set( seq)
    assert len(remainder) == len(seq)

    # node, remainding edges, cost
    state = 0, frozenset(remainder), 0

    reached = set()
    frontier = { state }

    def rm( fz, obj):
        s = set(fz)
        s.remove(obj)
        return frozenset(s)

    while frontier:
        print( len(frontier))
        new_frontier = set()
        for state in frontier:
            node, remaining_edges, cost = state
            for tup in seq:
                if tup not in remaining_edges: continue
                if tup[0] == node:
                    new_state = tup[1], rm(remaining_edges,tup), cost+tup[0]+tup[1]
                    new_frontier.add(new_state)
                elif tup[1] == node:
                    new_state = tup[0], rm(remaining_edges,tup), cost+tup[0]+tup[1]
                    new_frontier.add(new_state)

        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)


    M = None
    for node, remaining_edges, cost in reached:
        dist = len(seq)-len(remaining_edges)
        cand = dist, cost
        if M is None or cand > M: M = cand

    return M[1]

@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 31 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

def test_AA():
    with open("data0","rt") as fp:
        assert 19 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))



