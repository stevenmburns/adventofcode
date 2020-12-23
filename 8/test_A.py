
import io
import pytest

import logging
from logging import debug
import re

#logging.basicConfig(level=logging.DEBUG)

def parse(fp):
    p = re.compile("^(acc|jmp|nop) (\+|\-)(\d+)$")

    seq = []
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line
        inst = m.groups()[0]
        sgn = m.groups()[1]
        offset = m.groups()[2]
        if sgn == '-':
            offset = -int(offset)
        else:
            offset = int(offset)
        seq.append( (inst,offset))
    return seq


def exe( seq):
    acc = 0
    pc = 0

    executed = set()
    while 0 <= pc < len(seq):
        if pc in executed:
            return False, acc
        executed.add(pc)
        inst, offset = seq[pc]
        if inst == "nop":
            pc += 1
        elif inst == "acc":
            acc += offset
            pc += 1
        elif inst == "jmp":
            pc += offset
        else:
            assert False

    assert pc == len(seq)
    return True, acc


def main( fp):
    seq = parse(fp)
    return exe(seq)

def main2( fp):
    seq = parse(fp)

    terminates = []
    for i in range(len(seq)):
        inst, offset = seq[i]
        if inst == "jmp":
            seq[i] = "nop", offset
        elif inst == "nop":
            seq[i] = "jmp", offset
        pair = exe(seq)
        if pair[0]:
            terminates.append(pair[1])
        seq[i] = inst, offset

    assert len(terminates) == 1

    return terminates[0]

def test_A():
    txt = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""
    with io.StringIO(txt) as fp:
        assert (False,5) == main(fp)
    with io.StringIO(txt) as fp:
        assert 8 == main2(fp)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))
