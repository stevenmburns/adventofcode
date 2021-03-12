import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import json

import sys

logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( line)

    return seq


        



def step(nrows, ncols, onset, stuck):

    def neighbors( p):
        irow,icol = p
        for drow,dcol in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            jrow,jcol = irow+drow,icol+dcol
    
            if 0 <= jrow < nrows and 0 <= jcol < ncols:
                yield (jrow,jcol)


    frontier = set()
    for p in onset:
        frontier.add(p)
        for q in neighbors(p):
            frontier.add(q)

    new_onset = set( onset)
    for p in frontier:
        if p in stuck:
            continue

        count = sum( 1 for q in neighbors(p) if q in onset)
        if p in onset and count not in [2,3]:
            new_onset.remove(p)
        elif p not in onset and count in [3]:   
            new_onset.add(p)

    return new_onset

def print_board( nrows, ncols, onset):
    print()
    for irow in range(nrows):
        line = ''
        for icol in range(ncols):
            line += '#' if (irow,icol) in onset else '.'
        print(line)

def main(fp,*,nsteps,part2=False):
    seq = parse(fp)

    nrows = len(seq)
    ncols = len(seq[0])

    stuck = [(0,0),(nrows-1,0),(0,ncols-1),(nrows-1,ncols-1)] if part2 else []

    onset = set()
    for irow,line in enumerate(seq):
        for icol,c in enumerate(line):
            if c == '#':
                onset.add( (irow,icol))

    for p in stuck:
        onset.add( p)

    print_board( nrows, ncols, onset)
    for _ in range(nsteps):
        onset = step(nrows,ncols,onset,stuck)
        print_board( nrows, ncols, onset)

    return len(onset)

@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 4 == main(fp,nsteps=4)

@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp,nsteps=100))

#@pytest.mark.skip
def test_AA0():
    with open("data0", "rt") as fp:
        assert 17 == main(fp,nsteps=5,part2=True)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main(fp,nsteps=100,part2=True))


