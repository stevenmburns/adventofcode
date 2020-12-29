
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
    seq = list(cir.q)
    destination = cir.minus1( cir.current())
    while destination in seq[1:4]:
        destination = cir.minus1( destination)


    assert destination not in seq[:1]
    assert destination in seq[4:]

    idx = seq[4:].index(destination)
    assert 0 <= idx <= 5
    
    print('idx', idx)

    assert destination in seq[:1] or destination in seq[4:]

    seq = seq[4:idx+5] + seq[1:4] + seq[idx+5:] + seq[:1]

    return Circle(seq,cir.n)

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

