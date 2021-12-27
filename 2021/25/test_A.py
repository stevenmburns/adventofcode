from os import path
import pytest

from itertools import combinations, product
from collections import defaultdict, deque
from copy import deepcopy

def parse(fp):
    for line in fp:
        line = line.rstrip('\n')
        yield list(line)

def prnt(grid, tag='---'):
    print(tag)
    for row in grid:
        print(''.join(row))



def step(grid):
    # move east

    m = len(grid)
    n = len(grid[0])

    grid0 = deepcopy(grid)

    for i in range(m):
        for j in range(n):
            left = (j-1) % n
            if grid[i][left] == '>' and grid[i][j] == '.':
                grid0[i][j] = '>'
                grid0[i][left] = '.'

    grid1 = deepcopy(grid0)

    for i in range(m):
        for j in range(n):
            up = (i-1) % m
            if grid0[up][j] == 'v' and grid0[i][j] == '.':
                grid1[i][j] = 'v'
                grid1[up][j] = '.'

    return grid1, grid1 == grid

def main(fp):
    grid = list(parse(fp))
    count = 0
    prnt(grid, f'--- {count} ---')

    while True:
        grid, done = step(grid)
        count += 1
        prnt(grid, f'--- {count} ---')
        if done:
            return count

def main2(fp):
    ...

#@pytest.mark.skip
def test_A0():
    with open('data1', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))