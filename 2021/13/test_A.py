from functools import reduce
import pytest, re
from collections import defaultdict

def parse(fp):
    p = re.compile(r'^(\d+)\,(\d+)$')
    p_blank = re.compile(r'^\s*$')
    p_fold = re.compile(r'fold along (x|y)=(\d+)$')

    points = []

    folds = []

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        if m:
            points.append((int(m.groups()[0]), int(m.groups()[1])))
            continue
        m = p_blank.match(line)
        if m:
            continue
        m = p_fold.match(line)
        if m:
            folds.append((m.groups()[0], int(m.groups()[1])))
            continue

    return points, folds

def print_board(board):

    mx, Mx = min(x for x,_ in board), max(x for x,_ in board)
    my, My = min(y for _,y in board), max(y for _,y in board)

    for y in range(my, My+1):
        for x in range(mx, Mx+1):
            if (x, y) in board:
                print('#', end='')
            else:
                print('.', end='')
        print()



def main(fp):
    points, folds = list(parse(fp))

    board = set(points)

    for f in folds[:1]:
        axis, value = f
        print(axis, value)


        if axis == 'x':
            newboard0 = {(x,y) for x,y in board if x < value}
            newboard1 = {(value*2-x,y) for x,y in board if x > value}
        else:
            newboard0 = {(x,y) for x,y in board if y < value}
            newboard1 = {(x,2*value-y) for x,y in board if y > value}

        newboard = newboard0 | newboard1

    print('=====')
    print_board(board)
    print('=====')
    print_board(newboard)

    return len(newboard)

def main(fp):
    points, folds = list(parse(fp))

    board = set(points)

    for f in folds[:1]:
        axis, value = f
        print(axis, value)

        if axis == 'x':
            newboard0 = {(x,y) for x,y in board if x < value}
            newboard1 = {(value*2-x,y) for x,y in board if x > value}
        else:
            newboard0 = {(x,y) for x,y in board if y < value}
            newboard1 = {(x,2*value-y) for x,y in board if y > value}

        board = newboard0 | newboard1

    return len(board)




def main2(fp):
    points, folds = list(parse(fp))

    board = set(points)

    for f in folds:
        axis, value = f
        print(axis, value)


        if axis == 'x':
            newboard0 = {(x,y) for x,y in board if x < value}
            newboard1 = {(value*2-x,y) for x,y in board if x > value}
        else:
            newboard0 = {(x,y) for x,y in board if y < value}
            newboard1 = {(x,2*value-y) for x,y in board if y > value}

        board = newboard0 | newboard1

    print('=====')
    print_board(board)

def test_A0():
    with open('data0') as fp:
        assert 17 == main(fp)

#@pytest.mark.skip
def test_B():
    with open('data') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open('data0') as fp:
        main2(fp)

#@pytest.mark.skip
def test_BB():
    with open('data') as fp:
        main2(fp)
