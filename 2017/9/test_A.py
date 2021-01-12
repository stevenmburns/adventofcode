import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)

    return seq

def gen_tokens(line):
    i = 0
    state = 0
    garbage_count = 0
    while i < len(line):
        c = line[i]
        if c == '!':
            i += 2
            continue
        elif state == 0 and c == '<':
            state = 1
            i += 1
            continue
        elif state == 1 and c == '>':
            state = 0
            i += 1
            continue
        elif state == 0:
            yield c
            i += 1
        elif state == 1:
            garbage_count += 1
            i += 1
        else:
            assert False, (state, i)

    print( f'garbage_count: {garbage_count}')

def compute_score(line):
    score = 0
    depth = 0
    for c in gen_tokens(line):
        if c == '{':
            depth += 1
            score += depth
        elif c == '}':
            depth -= 1
    assert depth == 0
    return score

def main(fp):
    seq = parse(fp)

    score = 0
    for line in seq:
        score += compute_score(line)

    return score

@pytest.mark.skip
def test_A():
    with open("data0", "rt") as fp:
        assert 50 == main(fp)

def test_B():
    with open("data", "rt") as fp:
        print(main(fp))


