
import io
import pytest

import logging
from logging import debug
import re

from collections import deque
from copy import deepcopy

#logging.basicConfig(level=logging.DEBUG)

def parse(fp):
    p = re.compile(r'^([NSEWLRF])(\d+)$')

    seq = []
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        cmd = m.groups()[0]
        arg = int(m.groups()[1])

        if cmd in ['L', 'R']:
            assert arg % 90 == 0

        seq.append(( cmd, arg))
    return seq

def sim( seq):
    x = 0
    y = 0
    angle = 0

    for (cmd, arg) in seq:
        if cmd == 'N': y += arg
        elif cmd == 'S': y -= arg
        elif cmd == 'E': x += arg
        elif cmd == 'W': x -= arg
        elif cmd == 'L': angle = (angle + arg) % 360
        elif cmd == 'R': angle = (angle - arg) % 360
        elif cmd == 'F':
            if angle == 0: x += arg
            elif angle == 90: y += arg
            elif angle == 180: x -= arg
            elif angle == 270: y -= arg
            else:
                assert False, angle
        else:
            assert False, cmd
    
    return abs(x) + abs(y)

def sim2( seq):
    x = 0
    y = 0

    wx = 10
    wy = 1

    for (cmd, arg) in seq:
        if cmd == 'N': wy += arg
        elif cmd == 'S': wy -= arg
        elif cmd == 'E': wx += arg
        elif cmd == 'W': wx -= arg
        elif cmd == 'L' or cmd == 'R':
           if cmd == 'R': arg = -arg

           dx = wx - 0
           dy = wy - 0

           if arg % 360 == 0:
               pass
           elif arg % 360 == 90:
               dx, dy = -dy, dx
           elif arg % 360 == 180:
               dx, dy = -dx, -dy
           elif arg % 360 == 270:
               dx, dy =  dy, -dx
           else:
               assert False, arg
               
           wx = dx + 0
           wy = dy + 0

        elif cmd == 'F':
            x += arg*wx
            y += arg*wy
        else:
            assert False, cmd
    
    return abs(x) + abs(y)


def main( fp):
    seq = parse(fp)
    return sim(seq)

def main2( fp):
    seq = parse(fp)
    return sim2(seq)

def test_A():
    with open( "data0", "rt") as fp:
        assert 25 == main(fp)
    with open( "data0", "rt") as fp:
        assert 286 == main2(fp)


def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))

