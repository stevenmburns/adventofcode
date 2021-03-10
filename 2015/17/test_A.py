import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import json

import sys

logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( int(line))

    return seq

def main(fp,size=150):
    seq = parse(fp)
    print(seq)
    
    count = 0
    for i in range(1 << len(seq)):
        s = size
        for j in range(len(seq)):
            if i & (1<<j):
                s -= seq[j]
        if s == 0:
            count += 1

    return count

def main2_simple(fp,size=150):
    seq = parse(fp)
    print(seq)
    
    min_bits = None
    for i in range(1 << len(seq)):
        s = size
        bits = 0
        for j in range(len(seq)):
            if i & (1<<j):
                s -= seq[j]
                bits += 1
        if s == 0:
            if min_bits is None or min_bits > bits: min_bits = bits

    count = 0
    for i in range(1 << len(seq)):
        s = size
        bits = 0
        for j in range(len(seq)):
            if i & (1<<j):
                s -= seq[j]
                bits += 1
        if s == 0 and bits == min_bits:
            count += 1

    return count

def main(fp,size=150):
    seq = parse(fp)
    
    count = 0
    for k in range(1,len(seq)+1):
        for comb in itertools.combinations( seq, k):
            s = size
            for x in comb:
                s -= x
            if s == 0:
                count += 1
    return count

def main2(fp,size=150):
    seq = parse(fp)
    
    for k in range(1,len(seq)+1):
        count = 0
        for comb in itertools.combinations( seq, k):
            s = size
            for x in comb:
                s -= x
            if s == 0:
                count += 1
        if count > 0:
            return count

    return 0

#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 4 == main(fp,size=25)

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp,size=150))

#@pytest.mark.skip
def test_AA0():
    with open("data0", "rt") as fp:
        assert 3 == main2(fp,size=25)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp,size=150))

