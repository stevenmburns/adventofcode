import sys
import pytest
import io
import re
import itertools
from collections import deque

def knothash( n, txt):
    seq = [ ord(x) for x in txt]
    seq.extend( [17,31,73,47,23])
    seq = seq*64

    first = 0
    skip_size = 0
    lst = list(range(n))
    for length in seq:
        lst = lst[:length][::-1] + lst[length:]
        move_right = (length+skip_size)%n
        first = (first-move_right)%n
        lst = lst[move_right:] + lst[:move_right]
        skip_size += 1

    sparse_hash = lst[first:] + lst[:first]
    dense_hash = []
    for i in range(0,256,16):
        sum = 0
        for ii in range(i,i+16):
            sum = sum ^ sparse_hash[ii]
        dense_hash.append(sum)
    return dense_hash

def gen_board(txt):
    def toBits( x):
        return ''.join( '#' if x & (1<<j) != 0 else '.' for j in range(7,-1,-1))

    result = []
    for i in range(128):
        result.append( ''.join( toBits(x) for x in knothash(256,f'{txt}-{i}')))
    return result

def main(txt):
    board = gen_board(txt)

    count = 0
    for row in board:
        print(row)
        count += sum( 1 for c in row if c == '#')
    return count

def main2(txt):
    board = gen_board(txt)


    visited = {}
    partition = 0

    sys.setrecursionlimit(1600)

    k = 128

    for i in range(k):
        print( board[i][:k])


    dirs = [ (-1,0), (1,0), (0,-1), (0,1)]
    def gen_next( u):
        (i,j) = u
        for (di,dj) in dirs:
            ii, jj = i+di, j+dj
            if 0 <= ii < k and 0 <= jj < k and board[ii][jj] == '#':
                yield ii, jj

    def dfs( u):
        visited[u] = partition
        for v in gen_next(u):
            if v not in visited:
                dfs(v)

    for (i,j) in itertools.product( range(k), range(k)):
        if board[i][j] != '#':
            continue
        if (i,j) not in visited:
            dfs( (i,j))
            partition += 1

    return partition

@pytest.mark.skip
def test_A():
    assert 8108 == main('flqrgnkx')
def test_AA():
    assert 1242 == main2('flqrgnkx')

@pytest.mark.skip
def test_B():
    print(main('wenycdww'))

def test_BB():
    print(main2('wenycdww'))

