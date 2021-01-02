
import io
import pytest

import logging
from logging import debug
import re

import re
import collections
from collections import deque

class LinkListNode:
    def __init__(self, el, prev=None, next=None):
        self.el = el
        self.prev = prev
        self.next = next

class Circle:
    def __init__(self, seq, n=9):
        self.q = deque(seq + list(range(len(seq)+1,n+1)))
        self.n = n

        self.nodes = [None] + [ LinkListNode(i) for i in range(1,n+1)]

        last_x = seq[-1] if n == len(seq) else n

        for x in seq:
            self.nodes[last_x].next = self.nodes[x]
            self.nodes[x].prev = self.nodes[last_x]
            last_x = x
        for x in range(len(seq)+1,n+1):
            self.nodes[last_x].next = self.nodes[x]
            self.nodes[x].prev = self.nodes[last_x]
            last_x = x

        ptr = self.nodes[seq[0]]
        for x in self.q:
            assert ptr.el == x
            ptr = ptr.next
        for x in self.q:
            assert ptr.el == x
            ptr = ptr.next

        last_x = seq[-1] if n == len(seq) else n
        ptr = self.nodes[last_x]
        for x in reversed(self.q):
            assert ptr.el == x
            ptr = ptr.prev
        for x in reversed(self.q):
            assert ptr.el == x
            ptr = ptr.prev
        
        self.ptr = self.nodes[seq[0]]

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

    print(f'destination: {destination}')

    assert destination not in seq[:1]
    assert destination in seq[4:]

    idx = seq[4:].index(destination)
    
    assert destination in seq[:1] or destination in seq[4:]

    print( seq[4:idx+5], seq[1:4], seq[idx+5:], seq[:1])

    seq = seq[4:idx+5] + seq[1:4] + seq[idx+5:] + seq[:1]

    return Circle(seq,cir.n)

def step2( cir):

    seq_1_4 = [cir.ptr.next.el, cir.ptr.next.next.el, cir.ptr.next.next.next.el]

    destination = cir.minus1(cir.ptr.el)
    while destination in seq_1_4:
        destination = cir.minus1(destination)

    assert destination != cir.ptr.el
    assert destination not in seq_1_4

    # segments: seq_1_4[-1].next to destination
    # seq_1_4[0] to seq_1_4[-1]
    # destination.next to cir.ptr

    def connect( u, v):
        pu, pv = cir.nodes[u], cir.nodes[v]
        pu.next = pv
        pv.prev = pu

    u0 = cir.nodes[seq_1_4[-1]].next.el
    u1 = cir.nodes[destination].next.el
    u2 = cir.ptr.el

    connect( u2, u0)
    connect( destination, seq_1_4[0])
    connect( seq_1_4[-1], u1)

    cir.ptr = cir.nodes[u0]

    return cir

def main( fp):
    seq = parse(fp)

    cir = Circle( seq, len(seq))

    for _ in range(100):
        cir = step(cir)

    seq = list(cir.q)
    idx = seq.index(1)

    result = seq[idx+1:] + seq[0:idx]

    return ''.join( str(i) for i in result)

def main2( fp, n=1000000):
    seq = parse(fp)

    cir = Circle( seq, n)

    def list_to_seq(cir):
        ptr = cir.ptr
        s = [ptr.el]
        ptr = ptr.next
        while ptr != cir.ptr:
            s.append(ptr.el)
            ptr = ptr.next
        return s

    for i in range( 10*n):
        if i % (n/10) == 0:
            print(i)

        cir = step2(cir)

    if False:
        seq = list(cir.q)
        idx = seq.index(1)
        result = seq[idx:] + seq[:idx]

        print( 'result[1]', result[1])
        print( 'result[2]', result[2])
        return result[1]*result[2]
    else:
        while cir.ptr.el != 1:
            cir.ptr = cir.ptr.next
        return cir.ptr.next.el * cir.ptr.next.next.el

@pytest.mark.skip
def test_A():
    assert '67384529' == main( '389125467')
    assert 5568 == main2( '389125467',n=100)
    assert 430728 == main2( '389125467',n=1000)
    assert 149245887792 == main2( '389125467')


def test_C():
    pass
    print(main('952438716'))
    print(main2('952438716'))
