import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    p = re.compile( r'^(\d+): (\d+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line
        seq.append( (int(m.groups()[0]), int(m.groups()[1])))

    return seq

def main(fp):
    seq = parse(fp)

    cost = 0
    for p, l in seq:
        if p % (2*(l-1)) == 0:
            cost += p*l

    print(seq)
    return cost

import math

def main2(fp):
    seq = parse(fp)

    if False:
        offset = 0
        while True:
            caught = False
            for p, l in seq:
                if (p+offset) % (2*(l-1)) == 0:
                    caught = True
            if not caught:
                return offset
            offset += 1

    def lcm2( a, b):
        return a*b//math.gcd(a,b)

    seq.sort(key=lambda p: (p[1],p[0]))

    lcm = 1
    passthroughs = [0]
    for p, l in seq:
        m = 2*(l-1)
        new_lcm = lcm2( lcm, m)
        new_passthroughs = []
        for i in range(new_lcm//lcm):
            new_passthroughs.extend( [i*lcm+x for x in passthroughs])
        passthroughs = []
        for offset in new_passthroughs:
            if (p+offset) % m != 0:
                passthroughs.append(offset)
        lcm = new_lcm
        print(lcm,len(passthroughs))

    return passthroughs[0]



def test_A():
    with open("data0", "rt") as fp:
        assert 24 == main(fp)

def test_AA():
    with open("data0", "rt") as fp:
        assert 10 == main2(fp)

def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))





