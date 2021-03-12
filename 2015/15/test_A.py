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

    p = re.compile( r'^(\S+): capacity (\S+), durability (\S+), flavor (\S+), texture (\S+), calories (\S+)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line
        seq.append( (m.groups()[0], int(m.groups()[1]), int(m.groups()[2]), int(m.groups()[3]), int(m.groups()[4]), int(m.groups()[5])))

    return seq

def gen_tuples_loops( n, total):
    if n == 2:
        for i0 in range(total+1):
            i1 = total-i0
            yield (i0,i1)
    elif n == 4:
        for i0 in range(total+1):
            for i1 in range(total-i0+1):
                for i2 in range(total-i0-i1+1):
                    i3 = total-i0-i1-i2
                    yield (i0,i1,i2,i3)
    else:
        assert False, f'Not implemented for n={n}'

def gen_tuples( n, total):

    if n == 1:
        yield (total,)
    else:
        for i in range(total+1):
            for tup in gen_tuples( n-1, total-i):
                lst = deque(tup)
                lst.appendleft(i)
                yield tuple(lst)

def test_gen_tuples():
    assert list(gen_tuples(4,4)) == list(gen_tuples_loops( 4, 4))
    assert list(gen_tuples(2,10)) ==list(gen_tuples_loops( 2, 10))


def main(fp):
    seq = parse(fp)
    
    total = 100
    headers = ['capacity','durability','flavor','texture','calories']

    best_score = None

    for i_s in gen_tuples( len(seq), total):
        s = [ 0 for _ in range(len(seq[0])-1)]
        for c,tup in zip(i_s,seq):
            values = tup[1:]
            assert len(s) == len(values)
            for i in range(len(s)):
                s[i] += c*values[i]
        score = 1
        for x in s[:-1]:
            score *= max(0,x)
        if best_score is None or score > best_score: best_score = score

    return best_score

def main2(fp):
    seq = parse(fp)
    
    total = 100
    headers = ['capacity','durability','flavor','texture','calories']

    best_score = None

    for i_s in gen_tuples( len(seq), total):
        s = [ 0 for _ in range(len(seq[0])-1)]
        for c,tup in zip(i_s,seq):
            values = tup[1:]
            assert len(s) == len(values)
            for i in range(len(s)):
                s[i] += c*values[i]
        if s[-1] != 500: continue
        score = 1
        for x in s[:-1]:
            score *= max(0,x)
        if best_score is None or score > best_score: best_score = score

    return best_score

#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 62842880 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open("data0", "rt") as fp:
        assert 57600000 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))

