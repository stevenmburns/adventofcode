import pytest
import io
import re
import itertools
from collections import defaultdict

def parse(fp):

    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)

    assert len(seq) == 1

    return seq[0]

def annihilate( x, y):
    return x.lower() == y.lower() and (x.isupper() and y.islower() or x.islower() and y.isupper())


def check(line):
    for i in range(1,len(line)):
        if annihilate( line[i-1], line[i]):
            return False
    return True

def step(line):

    lst = list(line)
    if not lst:
        return ''

    nlst = [lst[0]]
    for idx in range(1,len(lst)):
        if nlst and annihilate( nlst[-1], lst[idx]):
            nlst.pop()
        else:
            nlst.append(lst[idx])
        #print(''.join(nlst),idx,''.join(lst),lst[idx])

    return ''.join(nlst)


def simple(line):
    s = line
    while True:
        news = step(s)
        if len(s) == len(news):
            return news
        s = news

def main(fp):
    line = parse(fp)
    print(len(line))

    result = simple(line)

    assert check(result)

    return len(result)

def main2(fp):
    line = parse(fp)
    print(len(line))

    units = set()
    for c in line:
        units.add(c.lower())

    m = None
    for u in units:
        lst = []
        for c in line:
            if c.lower() != u:
                lst.append(c)

        nline = ''.join(lst)
        result = simple(nline)
        #print(u, line, nline, result)
        assert check(result)

        cand = len(result)
        if m is None or cand < m: m = cand

    return m


@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 10 == main(fp)

@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 4 == main2(fp)

#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main2(fp))
