import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p = re.compile(r'^pos=<((|-)\d+),((|-)\d+),((|-)\d+)>, r=(\d+)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( ( (int(m.groups()[0]),int(m.groups()[2]),int(m.groups()[4])), int(m.groups()[6])))

    return seq


def main(fp):
    seq = parse(fp)

    def dist( p0, p1):
        sum = 0
        for c0, c1 in zip(p0,p1):
            sum += abs(c0-c1)
        return sum

    max_r, max_idx = max( [ (r,idx) for idx, (pos, r) in enumerate(seq)])
    print( max_r, max_idx)
    assert sum( 1 for (pos, r) in seq if r == max_r) == 1

    count_in_range_of_max = 0
    for (pos, r) in seq:
        if dist( pos, seq[max_idx][0]) <= max_r:
            count_in_range_of_max += 1

    return count_in_range_of_max

def main2(fp):
    seq = parse(fp)

    for (x,y,z), r in seq:
        print( y/x, z/x)

    def dist( p0, p1):
        sum = 0
        for c0, c1 in zip(p0,p1):
            sum += abs(c0-c1)
        return sum

    def count_in_range( p):
        return sum(1 for (pos, r) in seq if dist( pos, p) <= r)


    """
    It seems that we only need to consider points that are vertices
    of the simplex
"""

    candidate_points = set()

    def restrict( tup, plane):
        lb, ub = None, None
        """
        -r0 <= cx(x-x0) + cy(y-y0) + cz(z-z0) <= r0
        -r0 + cx x0 + cy y0 + cz z0 <= cx x + cy y + cz z <= r0 + cx x0 + cy y0 + cz z0
"""
        for (xx, yy, zz), rr in tup:
            cand = plane[0]*xx + plane[1]*yy + plane[2]*zz
            lcand = cand - rr
            if lb is None or lcand > lb: lb = lcand
            ucand = cand + rr
            if ub is None or ucand < ub: ub = ucand
            
        return lb, ub

    directions = [ (1,1,1), (-1,1,1), (1,-1,1), (1,1,-1)]
    count = 0
    for idx, tup in enumerate(itertools.combinations(seq,3)):
        tbl = {}
        for dir in directions:
            tbl[dir] = restrict( tup, dir)

        if all( lb <= ub for _, (lb,ub) in tbl.items()):
            count += 1
            num_equal = sum( 1 for _, (lb,ub) in tbl.items() if lb == ub)
            if num_equal > 0:
                print( '\t', num_equal, idx)
        if idx % 10000 == 0:
            print( idx, count)
    print(f'Number of combinations taken three at a time: {count}')

    lst = []
    for pos, r in seq:
        x,y,z = pos
        for xx,yy,zz in [(x-r,y,z),(x+r,y,z),
                         (x,y-r,z),(x,y+r,z),
                         (x,y,z-r),(x,y,z+r)]:
            c = count_in_range( (xx,yy,zz))
            logging.info( f'{(xx,yy,zz)} => {c}')
            lst.append( (c,dist( (xx,yy,zz), (0,0,0))))

    lst.sort()
    print( lst[-1])
    return lst[-1][1]

@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 7 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA():
    with open("data1","rt") as fp:
        assert 36 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))

