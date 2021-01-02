
import io
import pytest

import logging
from logging import debug
import re

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')

        seq.append( [ int(x) for x in line.split(',')])

    assert len(seq) == 1

    return seq[0]

def sim(lst,lmt):

    tbl = {}

    t = 0
    for x in lst[:-1]:
        tbl[x] = t
        t += 1

    current_x = lst[-1]
    while t < lmt-1:
        if current_x not in tbl:
            next_x = 0
        else:
            next_x = t - tbl[current_x]

        tbl[current_x] = t
        t += 1
        current_x = next_x

    return current_x



def main( fp,lmt=2020):
    lst = parse(fp)
    return sim(lst,lmt)



def test_A():
    with open( "data0", "rt") as fp:
        assert 436 == main(fp)
    with open( "data0", "rt") as fp:
        assert 175594 == main(fp,30*1000*1000)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main(fp,30*1000*1000))

