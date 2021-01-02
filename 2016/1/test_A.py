import io
import re

def parse(fp):

    seq = []

    p = re.compile(r'^([RL])(\d+)$')

    for line in fp:
        line = line.rstrip('\n')
        lst = []
        for s in line.split(', '):
            m = p.match(s)
            assert m
            lst.append( (m.groups()[0], int(m.groups()[1])))
        seq.append( lst)

    assert len(seq) == 1
    return seq[0]

def sim(lst):
    (x,y) = 0,0
    angle = 90
    tbl = { 0 : (1,0), 90: (0,1), 180: (-1,0), 270: (0,-1)}

    for dir, amount in lst:
        if dir == 'R':
            angle = (angle - 90) % 360
        elif dir == 'L':
            angle = (angle + 90) % 360
        else:
            assert False
    
        dx,dy = tbl[angle]
        x,y = x+amount*dx,y+amount*dy

    return abs(x)+abs(y)

def sim2(lst):
    (x,y) = 0,0
    angle = 90
    tbl = { 0 : (1,0), 90: (0,1), 180: (-1,0), 270: (0,-1)}

    visited = set()
    visited.add( (x,y))

    for dir, amount in lst:
        if dir == 'R':
            angle = (angle - 90) % 360
        elif dir == 'L':
            angle = (angle + 90) % 360
        else:
            assert False
    
        dx,dy = tbl[angle]
        for i in range(1,amount+1):
            x,y = x+dx,y+dy
            if (x,y) in visited:
                return abs(x)+abs(y)            
            visited.add( (x,y))

    return None

def main(fp):
    lst = parse(fp)
    return sim(lst)

def main2(fp):
    lst = parse(fp)
    return sim2(lst)

def test_A0():
    txt = """R2, L3
"""
    with io.StringIO( txt) as fp:
        assert 5 == main(fp)

def test_A1():
    txt = """R2, R2, R2
"""
    with io.StringIO( txt) as fp:
        assert 2 == main(fp)

def test_A2():
    txt = """R5, L5, R5, R3
"""
    with io.StringIO( txt) as fp:
        assert 12 == main(fp)

def test_A3():
    txt = """R8, R4, R4, R8
"""
    with io.StringIO( txt) as fp:
        assert 4 == main2(fp)

def test_B():
    with open( "data", "rt") as fp:
        print(main(fp))

    with open( "data", "rt") as fp:
        print(main2(fp))
