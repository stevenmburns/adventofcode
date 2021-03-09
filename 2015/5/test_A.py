import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import heapq

logging.basicConfig(level=logging.INFO)

def parse(fp):

    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)

    return seq

def isnice( line):
    def vowels(line):
        return sum(1 for c in line if c in "aeiou") >= 3

    twice_in_a_row = False
    bad = False
    for i in range(1,len(line)):
        a,b = line[i-1], line[i]
        if a == b:
            twice_in_a_row = True
        if (a+b) in ['ab','cd','pq','xy']:
            bad = True

    return vowels(line) and twice_in_a_row and not bad

def main(fp):

    seq = parse(fp)

    return sum( 1 for line in seq if isnice(line))

def isnice2( line):


    twice_in_a_row = False
    for i in range(2,len(line)):
        a,b,c = line[i-2], line[i-1], line[i]
        if a == c:
            twice_in_a_row = True


    rule1 = False
    for i in range(1,len(line)):
        a,b = line[i-1], line[i]
        for j in range(i+2,len(line)):
            c, d = line[j-1], line[j]
            if a == c and b == d:
                rule1 = True

    return rule1 and twice_in_a_row

def main2(fp):

    seq = parse(fp)

    return sum( 1 for line in seq if isnice2(line))


#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 1 == main(fp)

#@pytest.mark.skip
def test_A1():
    with open("data1", "rt") as fp:
        assert 1 == main(fp)

#@pytest.mark.skip
def test_A2():
    with open("data2", "rt") as fp:
        assert 0 == main(fp)

#@pytest.mark.skip
def test_A3():
    with open("data3", "rt") as fp:
        assert 0 == main(fp)

#@pytest.mark.skip
def test_A4():
    with open("data4", "rt") as fp:
        assert 0 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA5():
    with open("data5", "rt") as fp:
        assert 1 == main2(fp)

#@pytest.mark.skip
def test_AA6():
    with open("data6", "rt") as fp:
        assert 1 == main2(fp)

#@pytest.mark.skip
def test_AA7():
    with open("data7", "rt") as fp:
        assert 0 == main2(fp)

#@pytest.mark.skip
def test_AA8():
    with open("data8", "rt") as fp:
        assert 0 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))


