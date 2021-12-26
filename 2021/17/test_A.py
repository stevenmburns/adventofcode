import pytest
import io
from functools import reduce
from operator import add, mul
import re
from collections import defaultdict

def parse(fp):
    p = re.compile(r'^target area: x=((-|)\d+)\.\.((-|)\d+), y=((-|)\d+)\.\.((-|)\d+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        x0, _, x1, _, y0, _, y1, _ = m.groups()
        yield tuple(int(x) for x in (x0, x1, y0, y1))

class Probe:
    def __init__(self, vx, vy):
        self.x = 0
        self.y = 0
        self.vx = vx
        self.vy = vy

    def step(self):
        self.x += self.vx
        self.y += self.vy

        if self.vx < 0:
            self.vx += 1
        elif self.vx > 0:
            self.vx -= 1

        self.vy -= 1

def main(fp):
    x0, x1, y0, y1 = next(parse(fp))
    assert x0 <= x1 and y0 <= y1
    print(x0, x1, y0, y1)

    assert 0 <= x0

    xs = defaultdict(list)

    for vx0 in range(x1+1):
        probe0 = Probe(vx0, 0)
        for n in range(1, 1000):
            probe0.step()
            if x0 <= probe0.x <= x1:
                xs[vx0].append(n)

    tuples = []
    for vy0 in range(-1000,1001):
        for vx0, ns in xs.items():
            probe0 = Probe(vx0, vy0)
            set_ns = set(ns)
            max_y = 0
            for n in range(1, ns[-1]+1):
                probe0.step()
                max_y = max(max_y, probe0.y)
                if n in set_ns and y0 <= probe0.y <= y1:
                    tuples.append((max_y, n, vx0, vy0))


    best = max(tuples)
    all_initial_values = { (vx0, vy0) for _, _, vx0, vy0 in tuples }

    print(best, len(all_initial_values))

    return best[0], len(all_initial_values)

    

def test_A0():
    with open('data0', 'rt') as fp:
        assert (45, 112) == main(fp)

def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))




