import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append([ int(x) for x in line.split(',')])
    assert len(seq) == 1
    return seq[0]

def parse2(fp):
    p = re.compile(r'^(.*)(\s*)$')

    line = fp.read()

    m = p.match(line)
    assert m
    s = m.groups()[0]
    result = [ ord(x) for x in s]
    print( s, result)
    return result

def step( n, seq):
    first = 0
    skip_size = 0
    lst = list(range(n))
    #print(lst,first)
    for length in seq:
        lst = lst[:length][::-1] + lst[length:]
        move_right = (length+skip_size)%n
        first = (first-move_right)%n
        lst = lst[move_right:] + lst[:move_right]
        skip_size += 1
        #print(lst, first)
    return lst[first:] + lst[:first]

def main(fp,n):
    seq = parse(fp)
    lst = step( n, seq)
    return lst[0]*lst[1]

def main2(fp):
    n = 256
    seq = parse2(fp)

    seq.extend( [17,31,73,47,23])
    print(seq)

    lst = step(n, seq*64)

    dense_hash = []
    for i in range(0,256,16):
        sum = 0
        for ii in range(i,i+16):
            sum = sum ^ lst[ii]
        dense_hash.append(sum)

    result = ''.join( f'{i:02x}' for i in dense_hash)

    return result


def test_A():
    with open("data0", "rt") as fp:
        assert 12 == main(fp,5)

def test_AA0():
    txt = """
"""
    with io.StringIO(txt) as fp:
        assert 'a2582a3a0e66e6e86e3812dcb672a272' == main2(fp)

def test_AA1():
    txt = """AoC 2017
"""
    with io.StringIO(txt) as fp:
        assert '33efeb34ea91902bb2f59c9920caa6cd' == main2(fp)

def test_AA2():
    txt = """1,2,3
"""
    with io.StringIO(txt) as fp:
        assert '3efbe78a8d82f29979031a4aa0b16a9d' == main2(fp)

def test_AA3():
    txt = """1,2,4
"""
    with io.StringIO(txt) as fp:
        assert '63960835bcdc130f0b66d7ff4f6a5a8e' == main2(fp)

def test_B():
    with open("data", "rt") as fp:
        print(main(fp,256))

def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))


