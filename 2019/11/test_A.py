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

    while seq_tbl[pc] != 99:

        cmd = seq_tbl[pc]
        op = cmd % 100
        cmd = cmd // 100
        modebits = [op]
        for _ in range(3):
            modebits.append(cmd % 10)
            cmd = cmd // 10

        if op == 3:
            set_value_to_operand( modebits[1], seq_tbl[pc+1], (yield))
            pc += 2
        elif op == 4:
            yield get_operand( modebits[1], seq_tbl[pc+1])
            pc += 2
        elif op == 9:
            offset += get_operand( modebits[1], seq_tbl[pc+1])
            pc += 2
        elif op == 5:
            if get_operand( modebits[1], seq_tbl[pc+1]) != 0:
                pc = get_operand( modebits[2], seq_tbl[pc+2])
            else:
                pc += 3
        elif op == 6:
            if get_operand( modebits[1], seq_tbl[pc+1]) == 0:
                pc = get_operand( modebits[2], seq_tbl[pc+2])
            else:
                pc += 3
        elif op in insts:
            a = get_operand( modebits[1], seq_tbl[pc+1])
            b = get_operand( modebits[2], seq_tbl[pc+2])
            set_value_to_operand( modebits[3], seq_tbl[pc+3], insts[op]( a, b))
            pc += 4            
        else:
            assert False, modebits

def print_board( board, p, d):
    mrow, Mrow = -10, 10
    mcol, Mcol = -10, 10

    for (irow,icol) in board:
        if mrow is None or mrow > irow: mrow = irow 
        if Mrow is None or Mrow < irow: Mrow = irow 
        if mcol is None or mcol > icol: mcol = icol 
        if Mcol is None or Mcol < icol: Mcol = icol 

    print()
    for irow in range( mrow,Mrow+1):
        line = ''
        for icol in range( mcol,Mcol+1):
            q = (irow,icol) 
            if q == p:
                line += d
            elif q in board:
                line += '#'
            else:
                line += '.'
        print(line)


def main(fp,part2=False):
    insts = parse(fp)

    computer = gen_run(insts)        

    board = set()
    dirs = { '<': (0,-1), '>': (0,1), '^': (-1,0), 'v': (1,0)}
    order = '^<v>'

    def left( d):
        i = order.index(d)
        return order[(i+1)%4]

    def right( d):
        i = order.index(d)
        return order[(i-1)%4]

    p = 0, 0
    d = '^'

    if part2:
        board.add(p)

    print_board( board, p, d)

    painted_once = set()

    for _ in range(100000):
        try:
            next(computer)    
        except StopIteration:
            break

        painted_once.add(p)

        color = computer.send( 1 if p in board else 0)

        if color == 1:
            board.add(p)
        elif color == 0:
            if p in board:
                board.remove(p)
        else:
            assert False, color

        direction = next(computer)
        if direction == 0:
            d = left(d)
        elif direction == 1:
            d = right(d)
        else:
            assert False, direction

        p = tuple( x+dx for x,dx in zip( p, dirs[d]))

        print_board( board, p, d)

    return len(painted_once)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main(fp,True))




