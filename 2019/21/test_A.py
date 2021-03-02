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

import curses
import random

def main(fp):
    insts = parse(fp)

    computer = gen_run(insts)

    def recv():
        s = ''
        while True:
            try:
                rc = next(computer)
                if rc is None:
                    break
                if rc >= 128:
                    return s, rc
                s += chr(rc)
            except StopIteration:
                break
        return s, None

    def send( s):
        result = []
        for c in s:
            rc = computer.send(ord(c))
            assert rc is None
        rc = computer.send(ord('\n'))
        return rc


    _ = recv()

    prg = [ 'OR A J',
            'AND B J',
            'AND C J',
            'NOT J J',
            'AND D J']
            

    for line in prg:
        assert send( line) is None
    rc = send( 'WALK')
    
    txt, rc = recv()

    return rc

def main2(fp):
    insts = parse(fp)

    computer = gen_run(insts)

    def recv():
        s = ''
        while True:
            try:
                rc = next(computer)
                if rc is None:
                    break
                if rc >= 128:
                    return s, rc
                s += chr(rc)
            except StopIteration:
                break
        return s, None

    def send( s):
        result = []
        for c in s:
            rc = computer.send(ord(c))
            assert rc is None
        rc = computer.send(ord('\n'))
        return rc


    _ = recv()

    prg = [ 'NOT C J',
            'AND D J',
            'AND H J',

            'NOT B T',
            'AND D T',
            'OR T J',

            'NOT A T',
            'OR T J']
            

    for line in prg:
        assert send( line) is None
    rc = send( 'RUN')
    txt, rc = recv()

    return rc


#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))
