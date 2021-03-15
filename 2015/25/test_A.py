import hashlib
import pytest
import io
import re
import itertools
from functools import reduce
from collections import defaultdict, deque
import logging
import json

import sys

#logging.basicConfig(level=logging.INFO)

def diagonal( gen):
    icol, irow = 1, 1
    for x in gen:
        yield (irow, icol, x)
        if irow > 1:
            irow -= 1
            icol += 1
        else:
            irow = icol+1
            icol = 1

def test_diagonal():
    gen = diagonal( range(1,22))
    print( list(gen))


def randseq():
    x = 20151125
    f = 252533
    m = 33554393
    while True:
        yield x
        x = (x * f) % m

def main():
    gen = diagonal(randseq())
    while True:
        irow, icol, x = next(gen)
        if icol == 1:
            print(irow,icol,x)
        if irow == 3010 and icol == 3019:
            return x

    return None


#@pytest.mark.skip
def test_A0():
    assert 0 == main()

#@pytest.mark.skip
def test_B():
    print(main())
