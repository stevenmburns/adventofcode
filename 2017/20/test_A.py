import sys
import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    p_line = re.compile(r'^p=<\s*((|-)\d+)\s*,\s*((|-)\d+)\s*,\s*((|-)\d+)>\s*,\s*v=<\s*((|-)\d+)\s*,\s*((|-)\d+)\s*,\s*((|-)\d+)>\s*,\s*a=<\s*((|-)\d+)\s*,\s*((|-)\d+)\s*,\s*((|-)\d+)\s*>\s*$')
    for line in fp:
        line = line.rstrip('\n')
        m = p_line.match(line)
        assert m, line
        p = tuple( int(m.groups()[i]) for i in range(  0,  6, 2))
        v = tuple( int(m.groups()[i]) for i in range(  6, 12, 2))
        a = tuple( int(m.groups()[i]) for i in range( 12, 18, 2))

        seq.append( (p,v,a))

    return seq

def step( pva):
    p, v, a = pva
    v = v[0]+a[0], v[1]+a[1], v[2]+a[2]
    p = p[0]+v[0], p[1]+v[1], p[2]+v[2]
    return p, v, a


def compute_dists( pva, gen):
    p, v, a = pva
    dist = abs(p[0]) + abs(p[1]) + abs(p[2])
    dists = [dist]
    for _ in gen:
        p, v, a = step( (p, v, a))
        dist = abs(p[0]) + abs(p[1]) + abs(p[2])
        dists.append( dist)
    return dists


def traj( pva):
    dists = compute_dists( pva, range(3))

    """
    p + v*k + a*k*(k+1)/2

    k=0 => p 
    k=1 => p + 1*v +   a
    k=2 => p + 2*v + 3*a

    d0 = p
    d1 = p + 1*v + 1*a
    d2 = p + 2*v + 3*a
    d2 - 2*d1 + d0 = a
    d1 - d0 - a = v
"""
    pp = dists[0]
    aa = dists[2] - 2*dists[1] + dists[0]
    vv = dists[1] - dists[0] - aa

    if aa < 0 or aa == 0 and (vv < 0 or vv == 0 and pp < 0):
        pp, vv, aa = -pp, -vv, -aa

    assert aa >= 0

    return (pp,vv,aa)

def traj2( pva):
    p, v, a = pva
    dists = []
    sp, sv, sa = 0, 0, 0
    for t in range(3):
        pp, vv, aa = p[t], v[t], a[t]
        if aa < 0 or aa == 0 and (vv < 0 or vv == 0 and pp < 0):
            pp, vv, aa = -pp, -vv, -aa
        assert aa >= 0
        sp, sv, sa = sp+pp, sv+vv, sa+aa

    return (sp,sv,sa)


def remove_collisions( seq):
    tbl = {}
    for idx, pva in enumerate(seq):
        p, v, a = pva
        if p not in tbl: tbl[p] = []
        tbl[p].append( idx)
    new_seq = []
    for pva in seq:
        p, v, a = pva
        if len(tbl[p]) == 1:
            new_seq.append( pva)
    return new_seq

def main2(fp):
    seq = parse(fp)
    print(len(seq))
    seq = remove_collisions(seq)
    print(len(seq))
    for t in range(10000):
        new_seq = []
        for pva in seq:
            new_seq.append( step(pva))
        seq = remove_collisions(new_seq)
        print(len(seq))


def main(fp):
    seq = parse(fp)
    print(seq)

    tuples = []
    for idx, pva in enumerate(seq):
        cand0 = traj(pva)
        cand1 = traj2(pva)
        #assert cand0 == cand1
        tuples.append( (idx, cand1))
        
    tuples.sort( key=lambda p: (p[1][2], p[1][1], p[1][0], p[0])) 

    print( tuples[:10])

    best = tuples[0][0]

    print( len(seq))

    print(seq[0])

    
    s = []
    for i in range( len(tuples)):
        lst = compute_dists( seq[i], range(1000))
        s.append( (lst[-1], i))

    s.sort()

    print(s[:10])

    return s[0][1]

@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 0 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA():
    with open("data0","rt") as fp:
        assert 0 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))


