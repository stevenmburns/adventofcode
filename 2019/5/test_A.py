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

def run(seq,inps):
    print(seq,inps)

    pc = 0

    insts = { 1: lambda x,y: x+y,
              2: lambda x,y: x*y,
              7: lambda x,y: 1 if x < y else 0,
              8: lambda x,y: 1 if x == y else 0
    }

    outs = []

    def get_operand( mode, val):
        if mode == 0:
            return seq[val]
        else:
            return val

    while True:

        if seq[pc] == 99:
            break


        cmd = seq[pc]
        op = cmd % 100
        cmd = cmd // 100
        modebits = [op]
        for _ in range(4):
            modebits.append(cmd % 10)
            cmd = cmd // 10

        print(pc, modebits, seq[pc:pc+8])

        if op == 3:
            assert modebits[1] == 0
            seq[seq[pc+1]] = inps.popleft()
            pc += 2
        elif op == 4:
            outs.append( get_operand( modebits[1], seq[pc+1]))
            pc += 2
        elif op == 5:
            if get_operand( modebits[1], seq[pc+1]) != 0:
                pc = get_operand( modebits[2], seq[pc+2])
            else:
                pc += 3
        elif op == 6:
            if get_operand( modebits[1], seq[pc+1]) == 0:
                pc = get_operand( modebits[2], seq[pc+2])
            else:
                pc += 3
        elif op in insts:
            a = get_operand( modebits[1], seq[pc+1])
            b = get_operand( modebits[2], seq[pc+2])
            c = seq[pc+3]
            seq[seq[pc+3]] = insts[op]( a, b)
            pc += 4            
        else:
            assert False, modebits

    return outs

def main(fp,inps):
    seq = parse(fp)
    return run(seq[:],inps)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp,deque([1])))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main(fp,deque([5])))


