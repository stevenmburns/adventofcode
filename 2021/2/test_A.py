
import re

def parse(fp):
    p = re.compile(r'^(forward|down|up)\s+(\d+)\s*$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        yield (m.groups()[0], int(m.groups()[1]))

def main(fp):
    lst = list(parse(fp))
    p, d = 0, 0
    for (c, n) in lst:
        if c == 'forward':
            p += n
        elif c == 'down':
            d += n
        elif c == 'up':
            d -= n
        else:
            assert False
    return p*d

def main2(fp):
    lst = list(parse(fp))
    a, p, d = 0, 0, 0
    for (c, n) in lst:
        if c == 'forward':
            p += n
            d += a*n
        elif c == 'down':
            a += n
        elif c == 'up':
            a -= n
        else:
            assert False
    return p*d

def test_A():
    with open('data0') as fp:
        assert main(fp) == 150

def test_B():
    with open('data') as fp:
        assert main(fp) == 1989014

def test_AA():
    with open('data0') as fp:
        assert main2(fp) == 900

def test_BB():
    with open('data') as fp:
        assert main2(fp) == 2006917119