import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import json

import sys

#logging.basicConfig(level=logging.INFO)

def factor(k):
    factors = set()
    i = 1
    while i*i <= k:
        if k % i == 0:
            factors.add(i)
            factors.add(k//i)
        i += 1
    return factors

def test_factors():
    assert {1} == factor(1)
    assert {1,2} == factor(2)
    assert {1,3} == factor(3)
    assert {1,2,4} == factor(4)
    assert {1,5} == factor(5)

    print(factor(36000000))

def main(n):

    for k in range(1,n):
        if k % 10000 == 0:
            print(k)
        if sum( factor(k))*10 >= n:
            return k

    return None

def main2(n):

    houses = defaultdict(int)
    for k in range(1,831600*2):
        if k % 10000 == 0:
            print(k)
        for l in range(1,50):
            houses[k*l] += 11*k

    
    return min( k for k,v in houses.items() if v >= n)


@pytest.mark.skip
def test_B():
    print(main(36000000))

#@pytest.mark.skip
def test_BB():
    print(main2(36000000))
