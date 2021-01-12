import pytest
import io
import re
import itertools

def parse(fp):
    seq = []
    p = re.compile(r'^((|-)\d+)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( int(line))
    return seq

def sim(seq):
    pc = 0
    steps = 0
    while 0 <= pc < len(seq):
        new_pc = pc + seq[pc]
        seq[pc] += 1
        pc = new_pc
        steps += 1
    return steps

def main(fp):
    seq = parse(fp)
    
    return sim(seq)

def sim2(seq):
    pc = 0
    steps = 0
    while 0 <= pc < len(seq):
        offset = seq[pc]
        seq[pc] += -1 if offset >= 3 else 1
        pc += offset
        steps += 1
    return steps

def main2(fp):
    seq = parse(fp)
    
    return sim2(seq)

def test_A():
    with open("data0", "rt") as fp:
        assert 5 == main(fp)

def test_AA():
    with open("data0", "rt") as fp:
        assert 10 == main2(fp)

def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))

