import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    p = re.compile( r'^(\d+) <-> ((\d+)(, (\d+))*)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line
        seq.append( (int(m.groups()[0]), [int(s) for s in m.groups()[1].split(', ')]))

    return seq

def main(fp):
    seq = parse(fp)

    adjacent = dict(seq)

    visited = {}
    component = 0
    components = []

    def dfs( u):
        visited[u] = component
        for v in adjacent[u]:
            if v not in visited:
                dfs(v)
        
    for (u,_) in seq:
        if u not in visited:
            dfs(u)
            component += 1

    components = [ [] for _ in range(component)]
    for (k,v) in visited.items():
        components[v].append(k)

    return len(components[visited[0]]), len(components)

def test_A():
    with open("data0", "rt") as fp:
        assert (6,2) == main(fp)


def test_B():
    with open("data", "rt") as fp:
        print(main(fp))





