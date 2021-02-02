import pytest
import io
import re
import itertools
from collections import defaultdict

def pl(p,sn):
    x,y = p
    rackID = x + 10
    result = rackID*y
    result += sn
    result *= rackID
    result //= 100
    result %= 10
    result -= 5
    return result

def main(sn):
    n = 300
    best = None
    best_p = None
    for x in range(1,n+1-3+1):
        for y in range(1,n+1-3+1):
            sum = 0
            for xx in range(x,x+3):
                for yy in range(y,y+3):
                    sum += pl( (xx,yy), sn)
            if best is None or sum > best:
                best = sum
                best_p = x,y
    
    print( best, best_p)

    return best_p

def build_ctbl(sn,n):
    ctbl = defaultdict(int)
    for x in range(n+1,0,-1):
        for y in range(n+1,0,-1):
            sum = 0
            if x == n+1 or y == n+1:
                pass
            else:
                sum += pl( (x,y), sn)
                sum += ctbl[ (x,y+1)]
                sum += ctbl[ (x+1,y)]
                sum -= ctbl[ (x+1,y+1)]
            ctbl[ (x,y)] = sum
    return ctbl

def build_ctbl_slow(sn,n):
    ctbl = {}
    for x in range(n+1,0,-1):
        print(x)
        for y in range(n+1,0,-1):
            sum = 0 
            for xx in range(x,n+1):
                for yy in range(y,n+1):
                    sum += pl( (xx,yy), sn)
            ctbl[(x,y)] = sum
    return ctbl


def main2(sn):
    n = 300
    best = None
    best_p = None
    best_k = None

    ctbl = build_ctbl(sn,n)

    for k in range(1,n):
        if k % 20 == 0:
            print(f'k: {k}')
        for x in range(1,n+1-k+1):
            for y in range(1,n+1-k+1):
                sum = ctbl[ (x,y)] + ctbl[(x+k,y+k)]-ctbl[(x+k,y)]-ctbl[(x,y+k)]
                if best is None or sum > best:
                    best = sum
                    best_p = x,y
                    best_k = k
    
    print( best, best_p, best_k)

    return best_p[0], best_p[1], best_k

def test_ctbl():
    n = 3
    assert build_ctbl( 8, 3) == build_ctbl_slow( 8, 3)

def test_pl0():
    assert 4 == pl( (3,5), 8)
def test_pl1():
    assert -5 == pl( (122,79), 57)
def test_pl2():
    assert  0 == pl( (217,196), 39)
def test_pl3():
    assert  4 == pl( (101,153), 71)

@pytest.mark.skip
def test_A0():
    assert (33,45) == main(18)
@pytest.mark.skip
def test_A1():
    assert (21,61) == main(42)

#@pytest.mark.skip
def test_AA0():
    assert (90,269,16) == main2(18)
#@pytest.mark.skip
def test_AA1():
    assert (232,251,12) == main2(42)

#@pytest.mark.skip
def test_B():
    print(main(4455))

#@pytest.mark.skip
def test_BB():
    print(main2(4455))
