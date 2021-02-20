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

import curses
import random

def main(fp,part2=False):
    insts = parse(fp)

    computer = gen_run(insts)

    s = ''.join( chr(x) for x in computer)



    board = s.split('\n')[:-2]

    print(board)

    nrows = len(board)
    ncols = len(board[0])

    joints = set()
    for irow in range(1,nrows-1):
        assert len(board[irow]) == ncols
        for icol in range(1,ncols-1):
            if board[irow][icol] == '#' and \
               board[irow-1][icol] == '#' and \
               board[irow+1][icol] == '#' and \
               board[irow][icol-1] == '#' and \
               board[irow][icol+1] == '#':
                joints.add( (irow,icol))

    return sum( irow*icol for irow,icol in joints)


#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main(fp,part2=True))



