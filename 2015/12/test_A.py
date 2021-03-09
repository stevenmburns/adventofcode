import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import json

import sys

sys.setrecursionlimit(10000)


logging.basicConfig(level=logging.INFO)

def sum_integers( d):
    if type(d) == str:
        return 0
    if type(d) == dict:
        s = 0
        for k,v in d.items():
            if type(k) == int:
                s += k
            s += sum_integers( v)
        return s
    if type(d) == int:
        return d

    return sum( sum_integers(x) for x in d)

def sum_integers2( d):
    if type(d) == str:
        return 0
    if type(d) == dict:
        kill = False
        s = 0
        for k,v in d.items():
            if type(k) == int:
                s += k
            s += sum_integers2( v)
            if v == "red":
                kill = True
        return s if not kill else 0
    if type(d) == int:
        return d

    return sum( sum_integers2(x) for x in d)
        

def main(fp):
    d = json.load( fp)
    return sum_integers(d)

def main2(fp):
    d = json.load( fp)
    return sum_integers2(d)

@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 6 == main(fp)

@pytest.mark.skip
def test_A1():
    with open("data1", "rt") as fp:
        assert 6 == main(fp)

@pytest.mark.skip
def test_A2():
    with open("data2", "rt") as fp:
        assert 3 == main(fp)

@pytest.mark.skip
def test_A3():
    with open("data3", "rt") as fp:
        assert 3 == main(fp)

@pytest.mark.skip
def test_A4():
    with open("data4", "rt") as fp:
        assert 0 == main(fp)

@pytest.mark.skip
def test_A5():
    with open("data5", "rt") as fp:
        assert 0 == main(fp)

@pytest.mark.skip
def test_A6():
    with open("data6", "rt") as fp:
        assert 0 == main(fp)

@pytest.mark.skip
def test_A7():
    with open("data7", "rt") as fp:
        assert 0 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open("data0", "rt") as fp:
        assert 6 == main2(fp)

#@pytest.mark.skip
def test_AA8():
    with open("data8", "rt") as fp:
        assert 4 == main2(fp)

#@pytest.mark.skip
def test_AA9():
    with open("data9", "rt") as fp:
        assert 0 == main2(fp)

#@pytest.mark.skip
def test_AA10():
    with open("data10", "rt") as fp:
        assert 6 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))
        
