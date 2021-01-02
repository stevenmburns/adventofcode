
import io
import pytest

import logging
from logging import debug
import re

from collections import deque


#logging.basicConfig(level=logging.DEBUG)

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(int(line))
    return seq


def smallest_invalid( seq, preamble_size):
    q = deque(seq[:preamble_size])

    for x in seq[preamble_size:]:
        found = False
        for i in range(len(q)):
            for j in range(0,i):
                s = q[i] + q[j]
                if x == s:
                    found = True
        if not found:
            return x
        q.popleft()
        q.append(x)

    return None

def contiguous_match( seq, v):
    for i in range(len(seq)):
        for j in range(0,i):
            sum = 0
            for k in range(j,i+1):
                sum += seq[k]
            if sum == v:
                mn,mx = None, None
                for k in range(j,i+1):
                    if mn is None or seq[k] < mn:
                        mn = seq[k]
                    if mx is None or seq[k] > mx:
                        mx = seq[k]
                return mn+mx

    assert False

def main( fp, preamble_size):
    seq = parse(fp)

    return smallest_invalid(seq, preamble_size)

def main2( fp, preamble_size):
    seq = parse(fp)

    inv = smallest_invalid(seq, preamble_size)
    return contiguous_match(seq, inv)

def test_A():
    txt = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""
    with io.StringIO(txt) as fp:
        assert 127 == main(fp, 5)
    with io.StringIO(txt) as fp:
        assert 62 == main2(fp, 5)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp, 25))
    print("===")
    with open( "data", "rt") as fp:
        print(main2(fp, 25))
