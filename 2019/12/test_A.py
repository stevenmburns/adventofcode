import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import math

#logging.basicConfig(level=logging.INFO)

class Point:
    def __init__(self, p=(0,0,0)):
        self.p = p

    def __add__(self, q):
        return Point( tuple( px+qx for px,qx in zip( self.p, q)))

    def __sub__(self, q):
        return Point( tuple( px-qx for px,qx in zip( self.p, q)))

    def scale( self, s):
        return Point( tuple( s*px for px in self.p))

    def __repr__(self):
        return f'<x={self.p[0]}, y={self.p[1]}, z={self.p[2]}>'

    def accel(self, q):
        result = []
        for px,qx in zip( self.p, q):
            if px < qx:
                a = 1
            elif px > qx:
                a = -1
            else:
                a = 0
            result.append(a)
        return Point( tuple(result))

class Moon:
    def __init__(self, p):
        self.pos = Point(p)
        self.vel = Point()

    @property
    def potential_energy(self):
        return sum( abs(x) for x in self.pos.p)

    @property
    def kinetic_energy(self):
        return sum( abs(x) for x in self.vel.p)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy

    def __repr__(self):
        return f'pos={self.pos}, vel={self.vel}'

def parse(fp):
    seq = []

    p = re.compile( r'^<x=(\S+), y=(\S+), z=(\S+)>$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( tuple( int(x) for x in m.groups()))

    return seq

def print_moons( moons):
    print()
    for moon in moons:
        print(moon)


def step( moons):
    for moon0, moon1 in itertools.combinations( moons, 2):
        a = moon0.pos.accel( moon1.pos.p)
        moon0.vel = moon0.vel + a.p
        moon1.vel = moon1.vel - a.p

    for moon in moons:
        moon.pos = moon.pos + moon.vel.p


def main(fp,steps):
    seq = parse(fp)

    moons = [ Moon(p) for p in seq]

    def extract( moons, dim):
        v = []
        for moon in moons:
            v.extend( [ moon.pos.p[dim], moon.vel.p[dim]])
        return tuple(v)

    print_moons(moons)
    x_states = set()
    y_states = set()
    z_states = set()

    x_done, y_done, z_done = False, False, False

    for _ in range(steps):
        step(moons)

    print_moons(moons)

    return sum( moon.total_energy for moon in moons)

def main2(fp):
    seq = parse(fp)

    moons = [ Moon(p) for p in seq]

    def extract( moons, dim):
        v = []
        for moon in moons:
            v.extend( [ moon.pos.p[dim], moon.vel.p[dim]])
        return tuple(v)

    print_moons(moons)
    x_states = set()
    y_states = set()
    z_states = set()

    x_done, y_done, z_done = False, False, False

    while not x_done or not y_done or not z_done:
        step(moons)
        x_state = extract(moons, 0)
        y_state = extract(moons, 1)
        z_state = extract(moons, 2)
        if x_state not in x_states:
            x_states.add(x_state)
        else:
            x_done = True
        if y_state not in y_states:
            y_states.add(y_state)
        else:
            y_done = True
        if z_state not in z_states:
            z_states.add(z_state)
        else:
            z_done = True

    print_moons(moons)
    l = len(x_states), len(y_states), len(z_states)
    print(l)

    def lcm( x, y):
        f = math.gcd( x, y)
        return x*y//f

    return lcm( lcm( l[0], l[1]), l[2])

#@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 179 == main(fp,10)

#@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 1940 == main(fp,100)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp,1000))

#@pytest.mark.skip
def test_AA0():
    with open("data0","rt") as fp:
        assert 2772 == main2(fp)

#@pytest.mark.skip
def test_AA1():
    with open("data1","rt") as fp:
        assert 4686774924 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))




