import pytest
import io
import re
import itertools
from collections import defaultdict



def main(n):
    b = [3,7]
    elf0 = 0
    elf1 = 1
    while len(b) < 10+n:
        p = b[elf0] + b[elf1]
        if p > 9:
            b.append( p//10)
        b.append(p%10)
        elf0 = (elf0 + b[elf0] + 1) % len(b)
        elf1 = (elf1 + b[elf1] + 1) % len(b)
    return ''.join( str(x) for x in b[n:n+10])

def main2(s):
    lst = [int(c) for c in s]

    b = [3,7]
    elf0 = 0
    elf1 = 1
    for i in range(1000000000):
        p = b[elf0] + b[elf1]
        if p > 9:
            b.append( p//10)
        b.append(p%10)
        elf0 = (elf0 + b[elf0] + 1) % len(b)
        elf1 = (elf1 + b[elf1] + 1) % len(b)
        if len(b)-1 >= len(lst):
            if lst == b[-1-len(lst):-1]:
                return len(b)-1-len(lst)
        if len(b) >= len(lst):
            if lst == b[-len(lst):]:
                return len(b)-len(lst)

    return None


def test_A0():
    assert '5158916779' == main(9)
def test_A1():
    assert '0124515891' == main(5)
def test_A2():
    assert '9251071085' == main(18)
def test_A3():
    assert '5941429882' == main(2018)

@pytest.mark.skip
def test_B():
    print(main(323081))

def test_AA0():
    assert 9 == main2('51589')
def test_AA1():
    assert 5 == main2('01245')
def test_AA2():
    assert 18 == main2('92510')
def test_AA3():
    assert 2018 == main2('59414')

#@pytest.mark.skip
def test_B():
    print(main2('323081'))
    
