import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( [ int(x) for x in line.split(',')])

    assert len(seq) == 1

    return seq[0]

def run(seq,noun=12,verb=2):
    seq[1] = noun
    seq[2] = verb
    pc = 0
    while True:
        if seq[pc] == 99:
            break
        elif seq[pc] == 1:
            a = seq[pc+1]
            b = seq[pc+2]
            c = seq[pc+3]
            seq[c] = seq[a] + seq[b]
        elif seq[pc] == 2:
            a = seq[pc+1]
            b = seq[pc+2]
            c = seq[pc+3]
            seq[c] = seq[a] * seq[b]
        else:
            assert False, seq[pc]
        pc += 4
    return seq[0]

def main(fp):
    seq = parse(fp)
    return run(seq[:],12,2)

def main2(fp):
    seq = parse(fp)
    for noun in range(100):
        print(f'noun {noun}')
        for verb in range(100):
            if 19690720 == run(seq[:],noun,verb):
                return 100*noun+verb
    return None

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))


