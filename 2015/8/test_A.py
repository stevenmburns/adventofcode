import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO)

def parse(fp):

    seq = []
    for line in fp:
        line = line.rstrip('\n')
        assert line[0] == '"' and line[-1] == '"'
        seq.append(line)

    return seq

def extra(line):
    print(line)
    m = 0
    i = 1
    while i < len(line)-1:
        if line[i] == '\\':
            print('found backlash')
            if line[i+1] == '\\':
                m += 1
                i += 2
            elif line[i+1] == '"':
                m += 1
                i += 2
            elif line[i+1] == 'x':
                m += 1
                i += 4
            else:
                assert False, (line,i)
        else:
            m += 1
            i += 1

    return len(line)-m

def extra2(line):
    print(line)
    m = 2
    i = 0
    while i < len(line):
        if line[i] == '"':
            m += 2
            i += 1
        elif line[i] == '\\':
            m += 2
            i += 1
        else:
            m += 1
            i += 1

    return m-len(line)

def main(fp):
    seq = parse(fp)
    return sum( extra(line) for line in seq)

def main2(fp):
    seq = parse(fp)
    return sum( extra2(line) for line in seq)

#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 2 == main(fp)

#@pytest.mark.skip
def test_A1():
    with open("data1", "rt") as fp:
        assert 2 == main(fp)

#@pytest.mark.skip
def test_A2():
    with open("data2", "rt") as fp:
        assert 3 == main(fp)

#@pytest.mark.skip
def test_A3():
    with open("data3", "rt") as fp:
        assert 5 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open("data0", "rt") as fp:
        assert 4 == main2(fp)

#@pytest.mark.skip
def test_AA1():
    with open("data1", "rt") as fp:
        assert 4 == main2(fp)

#@pytest.mark.skip
def test_AA2():
    with open("data2", "rt") as fp:
        assert 6 == main2(fp)

#@pytest.mark.skip
def test_AA3():
    with open("data3", "rt") as fp:
        assert 5 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))
