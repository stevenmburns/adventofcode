import re
from itertools import combinations, product
from collections import defaultdict

def parse(fp):
    p = re.compile(r'^\s*(\d+),(\d+)\s*->\s*\s+(\d+),(\d+)\s*$')
    for line in fp:
        line = line.rstrip('\n')

        m = p.match(line)
        if m:
            x1, y1, x2, y2 = [int(i) for i in m.groups()]
            yield (x1, y1), (x2, y2)


def main(fp):
    lines = list(parse(fp))

    verticals = []
    horizontals = []

    for p1, p2 in lines:
        same_x = p1[0] == p2[0]
        same_y = p1[1] == p2[1]
        assert not (same_x and same_y)

        if same_x:
            verticals.append( (p1, p2))
        elif same_y:
            horizontals.append( (p1, p2))

    print(len(verticals), len(horizontals))

    doubles = set()

    for line1, line2 in product(verticals, horizontals):
        (x1, y1), (x2, y2) = line1 # vertical x1 == x2
        (x3, y3), (x4, y4) = line2 # horizontal y3 == y4

        assert x1 == x2
        assert y3 == y4

        if min(x3,x4) <= x1 <= max(x3,x4) and min(y1,y2) <= y3 <= max(y1,y2):
            doubles.add((x1, y3))

    for line1, line2 in combinations(horizontals, 2):
        (x1, y1), (x2, y2) = line1 # horizontal y1 == y2
        (x3, y3), (x4, y4) = line2 # horizontal y3 == y4

        assert y1 == y2
        assert y3 == y4

        if y1 == y3:
            for x in range(max(min(x1,x2), min(x3,x4)), 
                           min(max(x1,x2), max(x3,x4))+1):
                doubles.add((x, y1))

    for line1, line2 in combinations(verticals, 2):
        (x1, y1), (x2, y2) = line1 # vertical x1 == x2
        (x3, y3), (x4, y4) = line2 # vertical x3 == x4

        assert x1 == x2
        assert x3 == x4

        if x1 == x3:
            for y in range(max(min(y1,y2), min(y3,y4)), 
                           min(max(y1,y2), max(y3,y4))+1):
                doubles.add((x1, y))


    return len(doubles)

def main2(fp):
    lines = list(parse(fp))

    raster = defaultdict(list)

    for idx, (p0, p1) in enumerate(lines):


        def emit(t0, t1, dx, dy, x0, y0):
            for t in range(t0, t1+1):
                raster[(x0+t*dx,y0+t*dy)].append(idx)

        x0, y0 = p0
        x1, y1 = p1
        
        if x0 == x1: # vertical
            emit(min(y0,y1), max(y0,y1), 0, 1, x0, min(y0,y1))
        elif y0 == y1: # horizontal
            emit(min(x0,x1), max(x0,x1), 1, 0, min(x0,x1), y0)
        elif x0 < x1 and y0 < y1 or x0 > x1 and y0 > y1: # slope 1
            assert x1 - x0 == y1 - y0
            emit(min(x0,x1), max(x0,x1), 1, 1, min(x0,x1), min(y0,y1))
        elif x0 > x1 and y0 < y1 or x0 < x1 and y0 > y1: # slope -1
            assert x1 - x0 == y0 - y1
            emit(min(x0,x1), max(x0,x1), 1, -1, min(x0,x1), max(y0,y1))
        else:
            assert False

    print(raster)

    doubles = set()
    for (x,y), ids in raster.items():
        if len(ids) > 1:
            doubles.add((x,y))

    return len(doubles)


def test_A0():
    with open('data0') as fp:
        assert 5 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA0():
    with open('data0') as fp:
        assert 12 == main2(fp)

def xtest_BB():
    with open('data') as fp:
        print(main2(fp))