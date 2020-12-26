
import io
import pytest

import logging
from logging import debug
import re

def toMask( lst):
    result = 0
    for (idx,x) in enumerate(lst):
        if x:
            result |= 1 << idx
    return result

class Mask:
    def __init__(self,line):
        assert len(line) == 36
        self.ones = [x == '1' for x in reversed(line)]
        self.zeroes = [x == '0' for x in reversed(line)]
        self.xs = [x == 'X' for x in reversed(line)]

    def apply(self, x):
        return (x | toMask(self.ones)) & ~toMask(self.zeroes)


def parse(fp):
    p_mask = re.compile(r'^mask = ([01X]+)$')
    p_mem = re.compile(r'^mem\[(\d+)] = (\d+)$')

    seq = []
    for line in fp:
        line = line.rstrip('\n')

        m = p_mask.match(line)
        if m:
            seq.append(Mask(m.groups()[0]))
            continue

        m = p_mem.match(line)
        if m:
            seq.append( (int(m.groups()[0]), int(m.groups()[1])))
            continue

        assert False

    return seq

def sim(seq):
    mem = {}
    mask = None
    for x in seq:
        if type(x) == Mask:
            mask = x
        else:
            (addr,value) = x
            mem[addr] = mask.apply(value)

    sum = 0
    for (k,v) in mem.items():
        sum += v
    return sum

from itertools import product

def sim2(seq):
    mem = {}
    mask = None
    for x in seq:
        if type(x) == Mask:
            mask = x
        else:
            indices = [ idx for (idx,x) in enumerate(mask.xs) if x]

            pairs = [[0,1<<idx] for idx in indices]

            gen = product( *pairs)

            offsets = (sum(list(x)) for x in gen)

            (addr,value) = x

            addr0 = (addr | toMask(mask.ones)) & ~toMask(mask.xs)

            for o in offsets:
                mem[addr0 + o] = value

    s = 0
    for (k,v) in mem.items():
        s += v
    return s


def main( fp):
    seq = parse(fp)
    return sim(seq)

def main2( fp):
    seq = parse(fp)
    return sim2(seq)



@pytest.mark.skip
def test_A():
    with open( "data0", "rt") as fp:
        assert 165 == main(fp)

def test_B():
    with open( "data1", "rt") as fp:
        assert 208 == main2(fp)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))

