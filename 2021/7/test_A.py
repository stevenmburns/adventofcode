import re
from itertools import combinations, product
from collections import defaultdict, Counter

def parse(fp):
    for line in fp:
        line = line.rstrip('\n')
        yield from [int(x) for x in line.split(',')]


def main(fp):
    data = list(parse(fp))

    m, M = min(data), max(data)

    res = None

    for x in range(m, M+1):
        s = sum(abs(xx-x) for xx in data)
        if res is None or s < res:
            res = s

    return res

def main2(fp):
    data = list(parse(fp))

    m, M = min(data), max(data)

    def f(dist):
        n = abs(dist)
        return sum(i for i in range(1, n+1))

    res = None

    for x in range(m, M+1):
        s = sum(f(xx-x) for xx in data)
        if res is None or s < res:
            res = s

    return res

def test_A0():
    with open('data0') as fp:
        assert 37 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA0():
    with open('data0') as fp:
        assert 168 == main2(fp)

def test_BB():
    with open('data') as fp:
        print(main2(fp))