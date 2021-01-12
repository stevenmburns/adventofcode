import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    p = re.compile(r'^(\S+) (dec|inc) ((|-)\d+) if (\S+) (>=|==|<|!=|>|<=) ((|-)\d+)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        if m:
            seq.append( (m.groups()[0], m.groups()[1], int(m.groups()[2]),  m.groups()[4], m.groups()[5], int(m.groups()[6])))
            continue
        assert False, line

    return seq

def sim(seq):
    maxValue = None

    regs = {}
    def get_value( reg):
        if reg not in regs:
            regs[reg] = 0
        return regs[reg]

    def set_value( reg, v):
        nonlocal maxValue
        if maxValue is None or maxValue<v: maxValue = v
        regs[reg] = v

    for tup in seq:
        reg, cmd, amount, variable, cmp, target = tup
        if cmd == 'dec':
            amount = -amount
        cond = None
        if cmp == '<':
            cond = get_value(variable) < target
        elif cmp == '<=':
            cond = get_value(variable) <= target
        elif cmp == '>':
            cond = get_value(variable) > target
        elif cmp == '>=':
            cond = get_value(variable) >= target
        elif cmp == '==':
            cond = get_value(variable) == target
        elif cmp == '!=':
            cond = get_value(variable) != target
        else:
            assert False, cmp
        if cond:
            set_value( reg, get_value(reg) + amount)

    M = None
    for k,v in regs.items():
        if M is None or M<v: M = v
            
    return M, maxValue

def main(fp):
    seq = parse(fp)
    return sim(seq)


def test_A():
    with open("data0", "rt") as fp:
        assert (1,10) == main(fp)


def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

