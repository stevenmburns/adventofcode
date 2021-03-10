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

    p = re.compile( r'^Sue (\d+): (\S+): (\d+), (\S+): (\d+), (\S+): (\d+)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line
        seq.append( (int(m.groups()[0]), m.groups()[1], int(m.groups()[2]), m.groups()[3], int(m.groups()[4]), m.groups()[5], int(m.groups()[6])))

    return seq

def main(fp):
    seq = parse(fp)

    tbl = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }

    def check( tag, c):
        return tag not in tbl or tbl[tag] != c

    for tup in seq:
        sue, tag0, c0, tag1, c1, tag2, c2 = tup

        bad = False
        for tag,c in [(tag0,c0),(tag1,c1),(tag2,c2)]:
            if check(tag,c):
                bad = True
                continue

        if not bad:
            return sue

    return None

def main2(fp):
    seq = parse(fp)

    tbl = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }

    def mismatch( tag, c):
        if tag in ['cats','trees']:
            return tag not in tbl or tbl[tag] >= c
        elif tag in ['pomeranians','goldfish']:
            return tag not in tbl or tbl[tag] <= c
        else:
            return tag not in tbl or tbl[tag] != c

    for tup in seq:
        sue, tag0, c0, tag1, c1, tag2, c2 = tup

        bad = False
        for tag,c in [(tag0,c0),(tag1,c1),(tag2,c2)]:
            if mismatch(tag,c):
                bad = True
                continue

        if not bad:
            return sue

    return None


#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))

