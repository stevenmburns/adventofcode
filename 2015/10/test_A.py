import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO)

def step(txt):
    i = 0
    res = ''
    while i < len(txt):
        c = txt[i]
        j = i+1
        n = 1
        while j < len(txt) and c == txt[j]:
            j += 1
            n += 1
        assert j-i == n
        i = j

        assert n < 10

        res += str(n)
        res += c

    return res

def main(txt,repeat=1):
    for _ in range(repeat):
        txt = step(txt)

    return len(txt)

#@pytest.mark.skip
def test_A0():
    assert '11' == step('1')

#@pytest.mark.skip
def test_A1():
    assert '21' == step('11')

#@pytest.mark.skip
def test_A2():
    assert '1211' == step('21')

#@pytest.mark.skip
def test_A3():
    assert '111221' == step('1211')

#@pytest.mark.skip
def test_A4():
    assert '312211' == step('111221')

#@pytest.mark.skip
def test_B():
    print(main('3113322113',repeat=40))

#@pytest.mark.skip
def test_BB():
    print(main('3113322113',repeat=50))
