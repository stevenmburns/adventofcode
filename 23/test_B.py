
import io
import pytest

import logging
from logging import debug
import re

import re
import collections
from collections import deque

class Circle:
    def __init__(self, seq, n=9):
        self.q = deque(seq + list(range(len(seq)+1,n+1)))
        self.n = n

    def minus1(self, x):
        destination = x-1
        if destination == 0:
            destination = self.n
        return destination
    
    def current(self):
        return self.q[0]


def parse(txt):
    seq = [ int(c) for c in txt]
    return seq

def step( cir):
    print('Step')
    seq = list(cir.q)
    seq_0_1 = [ cir.q.popleft() for _ in range(1)]
    seq_1_4 = [ cir.q.popleft() for _ in range(3)]

    assert seq_0_1 == seq[:1]
    assert seq_1_4 == seq[1:4]

    destination = cir.minus1( seq_0_1[0])
    while destination in seq_1_4:
        destination = cir.minus1( destination)

    destination2 = cir.minus1( seq[0])
    while destination2 in seq[1:4]:
        destination2 = cir.minus1( destination2)

    assert destination2 == destination

    assert destination not in seq_0_1
    assert destination in cir.q

    idx = cir.q.index(destination)
    assert 0 <= idx <= 5
    
    print('idx', idx)

    assert destination in seq_0_1 or destination in cir.q

    seq_4_idxp5 = [ cir.q.popleft() for _ in range(idx+5-4)]

    assert seq_4_idxp5 == seq[4:idx+5]

    for x in seq_0_1:
        cir.q.append(x)

    for x in reversed( seq_1_4):
        cir.q.appendleft(x)

    for x in reversed( seq_4_idxp5):
        cir.q.appendleft(x)

    seq = seq[4:idx+5] + seq[1:4] + seq[idx+5:] + seq[:1]

    assert seq == list(cir.q)

    return cir

def main( fp):
    seq = parse(fp)

    cir = Circle( seq,len(seq))

    for _ in range(100):
        cir = step(cir)

    seq = list(cir.q)
    idx = seq.index(1)

    result = seq[idx+1:] + seq[0:idx]

    return ''.join( str(i) for i in result)

def main2( fp):
    seq = parse(fp)

    cir = Circle( seq,len(seq))

    for i in range(10000000):
        if i % 100000 == 0:
            print(i)
        cir = step(cir)

    seq = list(cir.seq)
    idx = seq.index(1)

    result = seq[idx+1:] + seq[0:idx]

    return result[1]*result[2]

def test_A():
    assert '67384529' == main( '389125467')
    #assert 149245887792 == main2( '389125467')

def test_C():
    print(main('952438716'))

