import re, pytest, io
from copy import deepcopy

def parse(fp):
    decode = None
    grid = []
    for idx, line in enumerate(fp):
        line = line.rstrip('\n')
        if idx == 0:
            print('decode', len(line))
            decode = line[:]
        elif idx == 1:
            assert line == ''
        else:
            grid.append(line)
    assert len(decode) == 512
    return decode, grid


def pad(grid, pad, pad_char='.'):
    m = len(grid)
    n = len(grid[0])
    new_grid = []
    for i in range(m+2*pad):
        new_row = ''
        for j in range(n+2*pad):
            if i < pad or i >= m+pad or j < pad or j >= n+pad:
                new_row += pad_char
            else:
                new_row += grid[i-pad][j-pad]
        new_grid.append(new_row)
    return new_grid

def prnt(grid):
    print("======")
    for row in grid:
        print(row)

def step(grid, decode):
    m = len(grid)
    n = len(grid[0])

    new_grid = []
    for i in range(m-3+1):
        new_row = ''
        for j in range(n-3+1):
            v = 0
            for di in range(3):
                for dj in range(3):
                    ii, jj = i+di, j+dj
                    v = (v<<1) | (1 if grid[ii][jj] == '#' else 0)

            p = decode[v]
            new_row += p
        new_grid.append(new_row)

    return new_grid

def count_on(grid):
    m = len(grid)
    n = len(grid[0])
    cnt = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '#':
                cnt += 1
    return cnt  


def main(fp):
    decode, grid = parse(fp)
    print(len(decode), len(grid), len(grid[0]))

    grid = pad(grid, 10)

    prnt(grid)

    grid = step(grid, decode)

    prnt(grid)

    grid = step(grid, decode)

    prnt(grid)
            

    return count_on(grid)

def main2(fp):
    decode, grid = parse(fp)
    print(len(decode), len(grid), len(grid[0]))

    grid = pad(grid, 10 + 2*50)

    flip = None
    if decode[0] == '#' and decode[-1] == '.':
        flip = True
    if decode[0] == '.' and decode[-1] == '#':
        flip = False

    assert flip is not None, (decode[0], decode[-1])



    prnt(grid)

    for idx in range(50):

        grid = step(grid, decode)

        prnt(grid)


            

    return count_on(grid)
    ...

@pytest.mark.skip
def test_A0():
    with open('data0', 'rt') as fp:
        assert 35 == main(fp)

@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA():
    with open('data0', 'rt') as fp:
        assert 3351 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))