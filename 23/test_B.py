
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

def step( cir, i=None):
    n = len(cir.q)

    seq_0_1 = [ cir.q.popleft() for _ in range(1)]
    seq_1_4 = [ cir.q.popleft() for _ in range(3)]

    destination = cir.minus1( seq_0_1[0])
    while destination in seq_1_4:
        destination = cir.minus1( destination)

    assert destination not in seq_0_1
    assert destination in cir.q

    for (idx,x) in enumerate(reversed(cir.q)):
        if destination == x:
            break
    idx = len(cir.q)-1-idx
    print(f"idx: {idx} {i} {idx+i}")

    



    assert destination in seq_0_1 or destination in cir.q

    print( n-(idx+5))

    seq_idxp5 = [ cir.q.pop() for _ in range(n-(idx+5))]

    #seq_4_idxp5 = [ cir.q.popleft() for _ in range(idx+5-4)]


    for x in seq_1_4:
        cir.q.append(x)

    for x in reversed(seq_idxp5):
        cir.q.append(x)

    for x in seq_0_1:
        cir.q.append(x)


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

    n = 1000*1000
    nsteps = 200

    cir = Circle( seq, n)

    for i in range(nsteps):
        if i % 100 == 0: print(i)
        cir = step(cir,i)

    seq = list(cir.q)
    idx = seq.index(1)

    result = seq[idx:] + seq[0:idx]

    print( 'result[1]', result[1])
    print( 'result[2]', result[2])

    return result[1]*result[2]

def test_A():
    #assert '67384529' == main( '389125467')
    assert 12 == main2( '389125467')

def test_C():
    pass
    #print(main('952438716'))
    #print(main2('952438716'))

if __name__ == "__main__":
    test_A()
