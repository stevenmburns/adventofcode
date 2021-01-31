import pytest
import io
import re
import itertools
from collections import defaultdict

def parse(fp):

    seq = []
    p = re.compile(r'^(\d+), (\d+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( (int(m.groups()[0]), int(m.groups()[1])))

    return seq

def main(fp):
    seq = parse(fp)

    mx, my, Mx, My = None, None, None, None

    for x,y in seq:
        if mx is None or x < mx: mx = x
        if Mx is None or x > Mx: Mx = x
        if my is None or y < my: my = y
        if My is None or y > My: My = y

    print(mx,my,Mx,My)

    dx,dy = Mx-mx, My-my
    llx, lly, urx, ury = mx-2*dx,my-2*dy,Mx+2*dx,My+2*dy

    print(llx,lly,urx,ury)

    tbl = {}
    for x in range(llx,urx+1):
        print( f'working on x {x}')
        for y in range(lly,ury+1):
            smallest = []
            best = None
            for idx,(xx,yy) in enumerate(seq):
                dist = abs(x-xx) + abs(y-yy)
                if best is None:
                    smallest = [idx]
                    best = dist
                elif best == dist:
                    smallest.append(idx)
                elif best > dist:
                    best = dist
                    smallest = [idx]
            tbl[ (x,y)] = None if len(smallest) != 1 else smallest[0]

    on_boundary = set()
    for x in range(llx,urx+1):
        for y in [lly,ury]:
            cand = tbl[(x,y)]
            if cand is not None:
                on_boundary.add(cand)
    for y in range(lly,ury+1):
        for x in [llx,urx]:
            cand = tbl[(x,y)]
            if cand is not None:
                on_boundary.add(cand)

    print(on_boundary)

    counts = defaultdict(int)
    for (x,y), v in tbl.items():
        if v is not None and v not in on_boundary:
            counts[v] += 1

    result = max( v for v in counts.values())

    print(counts, result)

    return result

def main2(fp,limit):
    seq = parse(fp)

    mx, my, Mx, My = None, None, None, None

    for x,y in seq:
        if mx is None or x < mx: mx = x
        if Mx is None or x > Mx: Mx = x
        if my is None or y < my: my = y
        if My is None or y > My: My = y

    print(mx,my,Mx,My)

    dx, dy = Mx-mx, My-my
    llx, lly, urx, ury = mx-1*dx,my-1*dy,Mx+1*dx,My+1*dy

    print(llx,lly,urx,ury)

    good = set()
    for x in range(llx,urx+1):
        if x % 100 == 0:
            print( f'working on x {x}')
        for y in range(lly,ury+1):
            sum = 0
            for xx,yy in seq:
                dist = abs(x-xx) + abs(y-yy)
                sum += dist
            if sum < limit:
                good.add((x,y))

    return len(good)

@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 17 == main(fp)
 
@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA():
    with open('data0', 'rt') as fp:
        assert 16 == main2(fp,32)

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp,10000))
