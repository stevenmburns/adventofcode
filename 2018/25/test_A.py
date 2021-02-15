import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p  = re.compile(r'^((|-)\d+),((|-)\d+),((|-)\d+),((|-)\d+)$')

    seq = []
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line
        seq.append( tuple( int(m.groups()[i]) for i in [0,2,4,6]))

    return seq

def dist( p0, p1):
    return sum( abs(u-v) for u,v in zip(p0,p1))
        
def equiv_points( p0, p1):
    return dist( p0, p1) <= 3

def equiv_sets( s0, s1):
    return any( equiv_points(p0,p1) for p0,p1 in itertools.product( s0, s1))

def main(fp):
    seq = parse(fp)

    sets = [ set( [x]) for x in seq]

    number_of_sets = len(sets)
    while True:
        print(number_of_sets)

        for (i0, i1) in itertools.combinations( range(len(sets)), 2):
            if equiv_sets(sets[i0],sets[i1]):
                lst = []
                for i,x in enumerate(sets):
                    if i == i0:
                        lst.append( sets[i0].union(sets[i1]))
                    elif i == i1:
                        pass
                    else:
                        lst.append( x)
                sets = lst
                break
            
        if number_of_sets == len(sets):
            break

        number_of_sets = len(sets)

    return number_of_sets


#@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 2 == main(fp)

#@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 4 == main(fp)

#@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        assert 3 == main(fp)

#@pytest.mark.skip
def test_A3():
    with open("data3","rt") as fp:
        assert 8 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))


