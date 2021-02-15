import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def check( num):
    digits = [ int(x) for x in str(num)]
    return any( x == y for x,y in zip(digits[:-1],digits[1:])) and \
        all( x <= y for x,y in zip(digits[:-1],digits[1:]))

def check2( num):
    if check(num):
        digits = [ int(x) for x in str(num)]
        for i in range(len(digits)-1):
            if digits[i] == digits[i+1]:
                if i-1 >= 0 and digits[i-1] == digits[i]:
                    pass
                elif i+2 < len(digits) and digits[i+1] == digits[i+2]:
                    pass
                else:
                    return True
    return False

def main(lb=402328,ub=864247):
    return sum( 1 for num in range(lb,ub+1) if check(num))

def main2(lb=402328,ub=864247):
    return sum( 1 for num in range(lb,ub+1) if check2(num))

#@pytest.mark.skip
def test_check():
    assert check( 111111)
    assert not check( 223450)
    assert not check( 123789)

#@pytest.mark.skip
def test_check2():
    assert check2( 112233)
    assert not check2( 123444)
    assert check2( 111122)

@pytest.mark.skip
def test_B():
    print(main())

#@pytest.mark.skip
def test_BB():
    print(main2())

