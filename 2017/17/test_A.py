import sys
import pytest
import io
import re
import itertools
from collections import deque

def step( a, steps_per_insert, i):
    k = (1+steps_per_insert) % len(a)
    return [i] + a[k:] + a[:k]


def main(steps_per_insert, total_times):
    a = [0]
    for i in range(1,total_times+1):
        a = step(a, steps_per_insert, i)
        print( a, a[(a.index(0)+1)%len(a)])
    return a[1]

class Node:
    def __init__(self, nm):
        self.nm = nm
        self.nxt = None

def main2(steps_per_insert, total_times):

    def prnt( ptr):
        result = [ptr.nxt.nm]
        q = ptr.nxt.nxt
        while q != ptr.nxt:
            result.append(q.nm)
            q = q.nxt
        print(result,end='')

    zero = Node(0)
    zero.nxt = zero
    ptr = zero
    prnt(ptr); print( '', zero.nxt.nm)

    nxt = [-1] * (total_times+1)


    for i in range(1,total_times+1):
        if i % 100000 == 0:
            print(i)
        for _ in range(steps_per_insert):
            ptr = ptr.nxt
        q = Node(i)
        q.nxt = ptr.nxt
        ptr.nxt = q
        ptr = q
        prnt(ptr); print( '', zero.nxt.nm)

    return zero.nxt.nm

def test_A0():
    print( main2( 345, 20))
def test_AA0():
    print( main( 345, 20))

@pytest.mark.skip
def test_A():
    assert 638 == main( 3, 2017)

@pytest.mark.skip
def test_B():
    print( main( 345, 2017))
