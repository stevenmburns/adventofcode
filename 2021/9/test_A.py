from os import rename
import re
from itertools import permutations, chain, product
from collections import defaultdict, Counter

def parse(fp):
    for line in fp:
        line = line.rstrip('\n')
        yield [int(x) for x in line]


def main(fp):
    data = list(parse(fp))

    m = len(data)
    n = len(data[0])

    def adjacent(i, j):
        p = [(0,1), (1,0), (0,-1), (-1,0)]
        for di, dj in p:
            if 0 <= i+di < m and 0 <= j+dj < n:
                yield i+di, j+dj

    mins = []
    for i, j in product(range(m), range(n)):
        if all(data[i][j] < data[i2][j2] for i2, j2 in adjacent(i, j)):
            mins.append((i, j))

    return sum(1+data[i][j] for i, j in mins)


def main2(fp):
    data = list(parse(fp))
    m = len(data)
    n = len(data[0])
    d = { (i,j): d for i, row in enumerate(data) for j, d in enumerate(row) }

    def adjacent(u):
        i, j = u
        for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
            if 0 <= i+di < m and 0 <= j+dj < n:
                yield i+di, j+dj

    reached = {}
    def dfs( u, basin):
        reached[u] = basin
        for v in adjacent(u):
            if v not in reached and d[v] != 9 and d[v] >= d[u]:
                dfs(v, basin)

    basin = 0
    for u in d:
        if all(d[u] < d[v] for v in adjacent(u)):
            if u not in reached and d[u] != 9:
                dfs(u, basin)
                basin += 1

    x,y,z = sorted(Counter(reached.values()).values(), reverse=True)[:3]
    return x*y*z

def test_A0():
    with open('data0') as fp:
        assert 15 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA0():
    with open('data0') as fp:
        assert 1134 == main2(fp)

def test_BB():
    with open('data') as fp:
        print(main2(fp))
