import sys
import pytest
import io
import re
import itertools
from collections import deque

def generator( seed, factor):
    while True:
        seed = (seed * factor) % 2147483647
        yield seed

def generator2( seed, factor, sieve):
    while True:
        seed = (seed * factor) % 2147483647
        if seed % sieve == 0:
            yield seed

def genA( seed):
    return generator( seed, 16807)

def genB( seed):
    return generator( seed, 48271)

def genA2( seed):
    return generator2( seed, 16807, 4)

def genB2( seed):
    return generator2( seed, 48271, 8)



def main(*, seedA, seedB):

    def low16( x):
        return x & ((1<<16)-1)

    count = 0
    for (idx,(x,y)) in zip(range(40*1000*1000),zip( genA( seedA), genB( seedB))):
        if idx % 1000000 == 0:
            print( idx)

        if low16(x) == low16(y):
            count += 1

    return count

def main2(*, seedA, seedB):

    def low16( x):
        return x & ((1<<16)-1)

    count = 0
    for (idx,(x,y)) in zip(range(5*1000*1000),zip( genA2( seedA), genB2( seedB))):
        if idx % 1000000 == 0:
            print( idx)

        if low16(x) == low16(y):
            count += 1

    return count

@pytest.mark.skip
def test_A():
    assert 588 == main( seedA=65, seedB=8921)

@pytest.mark.skip
def test_B():
    print( main( seedA=618, seedB=814))

def test_AA():
    assert 309 == main2( seedA=65, seedB=8921)

def test_BB():
    print( main2( seedA=618, seedB=814))


