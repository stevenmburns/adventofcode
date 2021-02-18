import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import math

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p = re.compile( r'^(\d+) (\S+)$')

    def pp(s):
        m = p.match(s)
        assert m
        return (int(m.groups()[0]), m.groups()[1])
 
    for line in fp:
        line = line.rstrip('\n')
        pair = line.split( " => ")
        assert len(pair) == 2

        lhs = [ pp(x) for x in pair[0].split( ', ')]
        rhs = pp(pair[1])
        
        seq.append( (lhs,rhs))

    return seq

import fractions

def main(fp,part2=False):
    seq = parse(fp)

    b = defaultdict(list)
    
    quanta = {}

    for (lhs,(r, v)) in seq:
        quanta[v] = r
        for l, u in lhs:
            b[v].append( (u,l))

    b['ORE'] = []
    quanta['ORE'] = 1

    order = deque()
    reach = set()
    def dfs( v):
        reach.add(v)
        for (u, _) in b[v]:
            if u not in reach:
                dfs( u)
        order.appendleft( v)

    dfs( 'FUEL')

    print(b)
    print(order)


 
    def require_ore( fuel):
        required = defaultdict(int)
        required['FUEL'] = fuel
        for v in order:
            r = quanta[v]
            required[v] = ((required[v] + r - 1) // r) * r
            for u, l in b[v]:
                required[u] += l*required[v]//r
        return required['ORE']

    if not part2:
        return require_ore( 1)
    else:
        target_ore = 1000000000000
        ub = 1
        while True:
            ore = require_ore(ub)
            if ore < target_ore:
                ub *= 2
            else:
                break
        
        lb = 1

        while lb+1 < ub:
            m = (lb+ub)//2
            ore = require_ore( m)
            if ore > target_ore:
                ub = m
            elif ore < target_ore:
                lb = m
                
        print(lb, require_ore(lb), ub, require_ore(ub))

        return lb

#@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 31 == main(fp)

#@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 165 == main(fp)

#@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        assert 13312 == main(fp)

#@pytest.mark.skip
def test_A3():
    with open("data3","rt") as fp:
        assert 180697 == main(fp)

#@pytest.mark.skip
def test_A4():
    with open("data4","rt") as fp:
        assert 2210736 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA2():
    with open("data2","rt") as fp:
        assert 82892753 == main(fp,True)

#@pytest.mark.skip
def test_AA3():
    with open("data3","rt") as fp:
        assert 5586022 == main(fp,True)

#@pytest.mark.skip
def test_AA4():
    with open("data4","rt") as fp:
        assert 460664 == main(fp,True)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main(fp,True))



