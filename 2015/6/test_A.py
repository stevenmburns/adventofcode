import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import heapq

logging.basicConfig(level=logging.INFO)

def parse(fp):

    p = re.compile( r'^(toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)$')

    seq = []
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( (m.groups()[0], int(m.groups()[1]), int(m.groups()[2]), int(m.groups()[3]), int(m.groups()[4])))

    return seq


def main(fp,n=1000):

    seq = parse(fp)
    print(seq)

    board = [ [ False for _ in range(n)] for _ in range(n)]

    for tup in seq:
        print(tup)
        if tup[0] == 'toggle':
            for x in range( tup[1], tup[3]+1):
                for y in range( tup[2], tup[4]+1):
                    board[x][y] = False if board[x][y] else True
        elif tup[0] == 'turn on':
            for x in range( tup[1], tup[3]+1):
                for y in range( tup[2], tup[4]+1):
                    board[x][y] = True
        elif tup[0] == 'turn off':
            for x in range( tup[1], tup[3]+1):
                for y in range( tup[2], tup[4]+1):
                    board[x][y] = False
        else:
            assert False, tup

    return sum( sum( 1 for x in line if x) for line in board)

def main2(fp,n=1000):

    seq = parse(fp)
    print(seq)

    board = [ [ 0 for _ in range(n)] for _ in range(n)]

    for tup in seq:
        print(tup)
        if tup[0] == 'toggle':
            for x in range( tup[1], tup[3]+1):
                for y in range( tup[2], tup[4]+1):
                    board[x][y] += 2
        elif tup[0] == 'turn on':
            for x in range( tup[1], tup[3]+1):
                for y in range( tup[2], tup[4]+1):
                    board[x][y] += 1
        elif tup[0] == 'turn off':
            for x in range( tup[1], tup[3]+1):
                for y in range( tup[2], tup[4]+1):
                    board[x][y] = max(0,board[x][y]-1)
        else:
            assert False, tup

    return sum( sum( x for x in line) for line in board)




#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 25 == main(fp,n=10)

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))


