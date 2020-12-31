
import io
import pytest

import logging
from logging import debug
import re

import re
import collections

def parse(fp):
    tbl = {}

    p_blank = re.compile(r"^$")
    p_row = re.compile(r"^([.#]+)$")
    p_tag = re.compile(r"^Tile (\d+):$")

    tag = None
    current = None
    for line in fp:
        line = line.rstrip('\n')
        m = p_blank.match(line)
        if m:
            tbl[tag] = current
            tag = None
            current = None
            continue
        m = p_tag.match(line)
        if m:
            tag = int(m.groups()[0])
            current = []
            continue
        m = p_row.match(line)
        if m:
            current.append( [ x == '#' for x in m.groups()[0]])
            continue

    assert tag is None and current is None
    return tbl

def el( board, x, y):
    return board[nrows-1-y][x]

def gen_borders( board):
    nrows = len(board)
    ncols = len(board[0])




def dihedral( ty, board):
    if ty == 'ROT90':
        


def main( fp):
    tbl = parse(fp)
    print(tbl)
    return 0

def test_A():
    with open( "data0", "rt") as fp:
        assert 0 == main(fp)

@pytest.mark.skip
def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
