import pytest
import io
import re
import hashlib
from math import gcd

def fill_disk(txt,sz):
    if len(txt) < sz:
        invtxt = ''.join( '1' if c == '0' else '0' for c in txt)
        new_txt = txt + '0' + invtxt[::-1]
        return fill_disk( new_txt, sz)
    elif len(txt) >= sz:
        return txt[:sz]

def gen_check_sum(data):
    assert len(data) % 2 == 0
    result = ''
    for i in range(0,len(data),2):
        if data[i] == data[i+1]:
            result += '1'
        else:
            result += '0'
    if len(result) % 2 == 1:
        return result
    else:
        return gen_check_sum(result)

def main(txt,sz):
    data = fill_disk( txt, sz)
    cksum = gen_check_sum( data)
    return cksum

def test_A():
    assert '01100' == main('10000',20)

#@pytest.mark.skip
def test_B():
    print( main('00101000101111010',272))
    print( main('00101000101111010',35651584))
