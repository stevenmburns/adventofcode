import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( [ int(x) for x in line.split(',')])

    assert len(seq) == 1

    return seq[0]

def gen_run(seq):
    pc = 0
    offset = 0

    seq_tbl = defaultdict(int)
    for idx,inst in enumerate(seq):
        seq_tbl[idx] = inst

    insts = { 1: lambda x,y: x+y,
              2: lambda x,y: x*y,
              7: lambda x,y: 1 if x < y else 0,
              8: lambda x,y: 1 if x == y else 0
    }

    jumps = { 5: lambda x: x != 0,
              6: lambda x: x == 0
    }

    def get_operand( mode, val):
        if mode == 0:
            return seq_tbl[val]
        elif mode == 1:
            return val
        elif mode == 2:
            return seq_tbl[val+offset]
        else:
            assert False, mode

    def set_value_to_operand( mode, val, value):
        if mode == 0:
            seq_tbl[val] = value
        elif mode == 1:
            assert False
        elif mode == 2:
            seq_tbl[val+offset] = value
        else:
            assert False, mode

    while True:
        cmd = seq_tbl[pc]
        op = cmd % 100


        cmd = cmd // 100
        modebits = [op]
        for _ in range(3):
            modebits.append(cmd % 10)
            cmd = cmd // 10

        if seq_tbl[pc] == 99:
            break

        if op == 3:
            set_value_to_operand( modebits[1], seq_tbl[pc+1], (yield))
            pc += 2
        elif op == 4:
            yield get_operand( modebits[1], seq_tbl[pc+1])
            pc += 2
        elif op == 9:
            offset += get_operand( modebits[1], seq_tbl[pc+1])
            pc += 2
        elif op in jumps:
            a = get_operand( modebits[1], seq_tbl[pc+1])
            b = get_operand( modebits[2], seq_tbl[pc+2])
            pc = b if jumps[op]( a) else pc+3
        elif op in insts:
            a = get_operand( modebits[1], seq_tbl[pc+1])
            b = get_operand( modebits[2], seq_tbl[pc+2])
            set_value_to_operand( modebits[3], seq_tbl[pc+3], insts[op]( a, b))
            pc += 4            
        else:
            assert False, modebits

import itertools

def main(fp):
    insts = parse(fp)

    N = 50
    onset = set()
    for irow,icol in itertools.product( range(N), range(N)):
        y,x = irow,icol

        computer = gen_run(insts)

        rc = next(computer)
        assert rc is None

        rc = computer.send(x)
        assert rc is None
        rc = computer.send(y)
        assert rc in [0,1]
        print( x,y,rc)
        if rc == 1:
            onset.add( (irow,icol))
        
    return len(onset)


class MockBoard:
    def __init__(self):
        self.board = []
        txt = """#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########
"""
        
        with io.StringIO(txt) as fp:
            for line in fp:
                line = line.rstrip('\n')
                self.board.append( line)

    def is_set( self, x, y):
        if y >= len(self.board):
            return False
        if x >= len(self.board[y]):
            return False
        return self.board[y][x] in '#O'


def main2(fp):

    use_mock = False

    if use_mock:
        mock = MockBoard()
        def is_set( x, y):
            return mock.is_set( x, y)
    else:

        insts = parse(fp)
        def is_set( x, y):
            computer = gen_run(insts)

            rc = next(computer)
            assert rc is None

            rc = computer.send(x)
            assert rc is None
            rc = computer.send(y)
            assert rc in [0,1]
            return rc == 1


    print()
    N = 50
    print( '   ' + '0'*10 + '1'*10 + '2'*10 + '3'*10 + '4'*10)
    print( '   ' + '0123456789'*5)

    for y in range(33,N):
        line = ''
        for x in range(N):
            line += '#' if is_set(x,y) else '.'
        print(f'{y:2d} {line}')


    if use_mock:
        M = 10
        starty = 1
        tbl_01 = { 0: 0}
        tbl_10 = { 0: 1}
    else:
        M = 100
        starty = 5
        tbl_01 = { 4: 5}
        tbl_10 = { 4: 6}


    def find_01( y):
        x = tbl_01[y-1]
        while not is_set(x,y):
            x += 1
        tbl_01[y] = x

    def find_10( y):
        x = tbl_10[y-1]
        while is_set(x,y):
            x += 1
        tbl_10[y] = x


    best = None
    for y in range(starty,100000):
        find_01(y)
        if y-(M-1) >= starty:
            find_10(y-(M-1))

            end =  tbl_10[y-(M-1)]
            start = tbl_01[y]

            if end-start >= M:
                best = (start, y-(M-1))
                break

    
    if False:
        for y in range(starty,best[1]+1):
            print( 'Checking', y)
            last = False
            for x in range(0, tbl_10[y]+10):
                cond = is_set(x,y)
                if not last and cond:
                    assert tbl_01[y] == x
                if last and not cond:
                    assert tbl_10[y] == x
                assert tbl_10[y] - tbl_01[y] >= 1
                last = cond

    best_x, best_y = best

    for y in range( best_y, best_y+M):
        for x in range( best_x, best_x+M):
            assert is_set( x, y), (best_x,best_y,x,y)


    return best_y + 10000*(best_x)


@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))



