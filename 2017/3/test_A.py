import pytest
import io
import re
import itertools

def main(n):
        
    def f(i):
        return (1 + i*2)**2
    layers = 0
    while f(layers) < n:
        layers += 1

    if layers == 0:
        assert n == 1
        return 0

    lb = f(layers-1)+1
    ub = f(layers)+1

    assert (ub-lb) % 4 == 0
    
    pos = (n-lb) % (2*layers) - layers + 1
    
    print( n, layers, pos)

    return layers + abs(pos)

def gen_spiral():
    yield 1, (0,0)

    p = 2
    layers = 1
    while True:
        # East
        for q in range(2*layers):
            yield p, (layers, q-layers+1)
            p += 1
        # North
        for q in range(2*layers):
            yield p, (layers-q-1, layers)
            p += 1
        # West
        for q in range(2*layers):
            yield p, (-layers, layers-q-1)
            p += 1
        # South
        for q in range(2*layers):
            yield p, (q-layers+1, -layers)
            p += 1
        layers += 1

def mainalt(n):
    for (i,(x,y)) in gen_spiral():
        if i == n:
            return abs(x)+abs(y)

main = mainalt

def gen_spiral2():
    tbl = {}
    dirs = [ (-1,0), (1,0), (0,-1), (0,1), (-1,1), (1,1), (-1,-1), (1,-1)]
    for (i,(x,y)) in gen_spiral():
        sum = 0
        if i == 1:
            sum = 1
        else:
            for dx,dy in dirs:
                xx,yy = x+dx,y+dy
                if (xx,yy) in tbl:
                    sum += tbl[(xx,yy)]
        tbl[(x,y)] = sum
        yield i, sum
            

def main2(n):
    for i,v in gen_spiral2():
        if v > n:
            return v

#@pytest.mark.skip
def test_A0():
    assert 0 == main(1)
def test_A1():
    assert 3 == main(12)
def test_A2():
    assert 2 == main(23)
def test_A3():
    assert 4 == main(25)
def test_A4():
    assert 5 == main(26)
#@pytest.mark.skip
def test_A5():
    assert 31 == main(1024)


#@pytest.mark.skip
def test_B():
    print(main(277678))

def test_BB():
    #print(main2(277678))
    print(main2(277678))

