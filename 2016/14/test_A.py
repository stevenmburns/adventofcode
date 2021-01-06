import pytest
import io
import re
import hashlib

def main(*,salt):

    memo = {}

    def f(idx):
        if idx in memo:
            return memo[idx]
        base = f'{salt}{idx}'
        result = hashlib.md5(base.encode()).hexdigest()
        memo[idx] = result
        return result

    hexdigits = '0123456789abcdef'

    def check_triple( hexdigest):
        for i in range(len(hexdigest)-2):
            for digit in hexdigits:
                if digit*3 == hexdigest[i:i+3]:
                    return digit
        return None

    def check_quint( idx, digit):
        for i in range(1000):
            hexdigest = f(idx+1+i)
            if digit*5 in hexdigest:
                return True
        return False

    idx = 0
    keys = []
    while True:
        hexdigest = f(idx)
        digit = check_triple(hexdigest)

        if digit is not None:
            if check_quint( idx, digit):
                keys.append( hexdigest)
        
        if len(keys) == 64:
            return idx
        idx += 1

def main2(*,salt):

    memo = {}

    def f(idx):
        if idx in memo:
            return memo[idx]
        base = f'{salt}{idx}'
        result = hashlib.md5(base.encode()).hexdigest()
        for _ in range(2016):
            result = hashlib.md5(result.encode()).hexdigest()
        memo[idx] = result
        return result

    hexdigits = '0123456789abcdef'

    def check_triple( hexdigest):
        for i in range(len(hexdigest)-2):
            for digit in hexdigits:
                if digit*3 == hexdigest[i:i+3]:
                    return digit
        return None

    def check_quint( idx, digit):
        for i in range(1000):
            hexdigest = f(idx+1+i)
            if digit*5 in hexdigest:
                return True
        return False

    idx = 0
    keys = []
    while True:
        hexdigest = f(idx)
        digit = check_triple(hexdigest)

        if digit is not None:
            if check_quint( idx, digit):
                keys.append( hexdigest)
        
        if len(keys) == 64:
            return idx
        idx += 1



def test_A():
    assert 22728 == main(salt='abc')
    assert 22551 == main2(salt='abc')

#@pytest.mark.skip
def test_B():
    print(main(salt='yjdafjpo'))
    print(main2(salt='yjdafjpo'))

