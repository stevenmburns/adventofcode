import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import json

import sys

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p_one = re.compile(r'^(inc|tpl|hlf) (a|b)$')
    p_jmp = re.compile(r'^(jmp) ((\+|\-)\d+)$')
    p_cond_jmp = re.compile(r'^(jie|jio) (a|b), ((\+|\-)\d+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p_one.match(line)
        if m:
            seq.append( m.groups())
            continue
        m = p_jmp.match(line)
        if m:
            seq.append( (m.groups()[0], int(m.groups()[1])))
            continue
        m = p_cond_jmp.match(line)
        if m:
            seq.append( (m.groups()[0], m.groups()[1], int(m.groups()[2])))
            continue

    return seq

def main(fp,starting_a=0):
    instructions = parse(fp)

    pc = 0
    regs = { 'a': starting_a, 'b': 0}

    while 0 <= pc < len(instructions):
        inst = instructions[pc]
        print(pc,regs,inst,end=' => ')
        if inst[0] == 'hlf':
            assert regs[inst[1]] % 2 == 0
            regs[inst[1]] //= 2
            pc += 1
        elif inst[0] == 'tpl':
            regs[inst[1]] *= 3
            pc += 1
        elif inst[0] == 'inc':
            regs[inst[1]] += 1
            pc += 1
        elif inst[0] == 'jmp':
            pc += inst[1]
        elif inst[0] == 'jie':
            if regs[inst[1]] % 2 == 0:
                pc += inst[2]
            else:
                pc += 1
        elif inst[0] == 'jio':
            if regs[inst[1]] == 1:
                pc += inst[2]
            else:
                pc += 1
        else:
            assert False, inst
        print(pc,regs)
                

    print(regs)
    return regs['a']

#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 2 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp,starting_a=1))
