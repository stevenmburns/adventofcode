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

#@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        insts = parse(fp)

        computer = gen_run(insts)

        assert insts == list(computer)

#@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        insts = parse(fp)

        computer = gen_run(insts)

        outs = list(computer)

        assert len(outs) == 1
        assert len(str(outs[0])) == 16

#@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        insts = parse(fp)

        computer = gen_run(insts)

        outs = list(computer)

        assert len(outs) == 1
        assert outs[0] == 1125899906842624

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        insts = parse(fp)

        computer = gen_run(insts)        
        next(computer)

        print( computer.send(1))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        insts = parse(fp)

        computer = gen_run(insts)        
        next(computer)

        print( computer.send(2))



