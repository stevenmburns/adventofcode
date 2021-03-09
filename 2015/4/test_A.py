import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import heapq

logging.basicConfig(level=logging.INFO)

def h( txt):
    return hashlib.md5(txt.encode()).hexdigest()

def main(key):
    x = 1
    while True:
        txt = f'{key}{x}'
        hh = h(txt)
        if hh[:5] == '00000':
            return x
        x += 1

def main2(key):
    x = 1
    while True:
        txt = f'{key}{x}'
        hh = h(txt)
        if hh[:6] == '000000':
            return x
        x += 1

#@pytest.mark.skip
def test_A0():
    assert 609043 == main('abcdef')

#@pytest.mark.skip
def test_A1():
    assert 1048970 == main('pqrstuv')

#@pytest.mark.skip
def test_B():
    print(main('yzbqklnj'))

#@pytest.mark.skip
def test_BB():
    print(main2('yzbqklnj'))

