import sys
import pytest
import io
import re
import itertools
from collections import deque

import array

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

    nxt = array.array('l',[-1] * (total_times+1))

    def prnt( ptr):
        result = [nxt[ptr]]
        q = nxt[nxt[ptr]]
        while q != nxt[ptr]:
            result.append(q)
            q = nxt[q]
        print(result,end='')

    zero = 0
    nxt[0] = 0
    #prnt(zero); print( '', nxt[zero])
    ptr = nxt[0]

    for i in range(1,total_times+1):
        if i % 100000 == 0:
            print(i)
        for _ in range(steps_per_insert):
            ptr = nxt[ptr]
        nxt[i] = nxt[ptr]
        nxt[ptr] = i
        ptr = i
        #prnt(ptr); print( '', nxt[zero])

    return nxt[zero]

def test_A0():
    print( main2( 345, 50*1000*1000))

@pytest.mark.skip
def test_AA0():
    print( main( 345, 20))

@pytest.mark.skip
def test_A():
    assert 638 == main( 3, 2017)

@pytest.mark.skip
def test_B():
    print( main( 345, 2017))

if __name__ == "__main__":
    print( main2( 345, 50*1000*1000))    
