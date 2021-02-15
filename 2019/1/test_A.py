import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p  = re.compile(r'^((|-)\d+)$')
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line
        seq.append( int(m.groups()[0]))

    return seq

def fuel(m):
    return m // 3 - 2

def limit(f):
    af = f
    while af > 0:
        af = max(0,fuel(af))
        f += af
    return f

def main(fp):
    seq = parse(fp)
    return sum( fuel(m) for m in seq)

def main2(fp):
    seq = parse(fp)
    return sum( limit(fuel(m)) for m in seq)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))


