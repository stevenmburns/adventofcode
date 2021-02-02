import pytest
import io
import re
import itertools
from collections import defaultdict

def parse(fp):
    seq = []
    p = re.compile('^position=<\s*((|-)\d+),\s*((|-)\d+)\s*> velocity=<\s*((|-)\d+),\s*((|-)\d+)\s*>\s*$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        
        position = int(m.groups()[0]), int(m.groups()[2])
        velocity = int(m.groups()[4]), int(m.groups()[6])

        seq.append( (position,velocity))

    return seq


def main(fp):
    seq = parse(fp)
    print(seq)

    values = []
    for t in range(20000):
        sum_sq = 0,0
        sum = 0,0
        for p, v in seq:
            pp = p[0]+v[0]*t, p[1]+v[1]*t
            sum_sq = sum_sq[0] + pp[0]**2, sum_sq[1] + pp[1]**2
            sum = sum[0] + pp[0], sum[1] + pp[1]
        
        n = len(seq)
        x_dist2 = sum_sq[0]/n - (sum[0]/n)**2
        y_dist2 = sum_sq[1]/n - (sum[1]/n)**2

        values.append( (x_dist2+y_dist2, t))

    """
    sum_i (x_i - x_)^2 = sum_i x_i ** 2 - 2 * x_i * x_ + x_ ** 2

    n * x_ = sum_i x_i

    sum_i (x_i ** 2) - 2 * (sum_i (x_i)) ** 2 / n + (sum_i x_i) ** 2  / n**2  
"""

    min_d, min_t = min(values)

    sky = defaultdict(lambda: '.')

    llx, lly, urx, ury = None, None, None, None

    for p,v in seq:
        pp = p[0]+v[0]*min_t, p[1]+v[1]*min_t
        sky[pp] = '#'

        if llx is None or llx > pp[0]: llx = pp[0]
        if lly is None or lly > pp[1]: lly = pp[1]
        if urx is None or urx < pp[0]: urx = pp[0]
        if ury is None or ury < pp[1]: ury = pp[1]

    print(llx,lly,urx,ury)
    
    for y in range(lly,ury+1):
        line = ''
        for x in range(llx,urx+1):
            line += sky[(x,y)]
        print(line)
            

    return min_t

def test_A():
    with open("data0","rt") as fp:
        assert 3 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))
