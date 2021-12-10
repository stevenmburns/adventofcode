from os import rename
import re
from itertools import permutations, chain, product
from collections import defaultdict, Counter, deque

def parse(fp):
    for line in fp:
        yield line.rstrip('\n')

m = { '{':'}', '[':']', '(':')', '<':'>' }

def aux(line):
    stack = []
    im = { v: k for k, v in m.items() }
    for c in line:
        if c in m:
            stack.append(c)
        elif c in im:
            if not stack or im[c] != stack[-1]:
                return c, stack
            stack.pop()
    else:
        return None, stack

def main(fp):
    tbl = { ')' : 3, '}' : 1197, ']' : 57, '>' : 25137 }
    return sum(tbl[c] if (c := aux(line)[0]) is not None else 0
                for line in  parse(fp))

def main2(fp):
    tbl = { ')' : 1, '}' : 3, ']' : 2, '>' : 4 }

    scores = []
    for line in parse(fp):
        c, stack = aux(line)
        if c is None:
            score = 0
            while stack:
                cc = stack.pop()
                score = score*5 + tbl[m[cc]]

            scores.append(score)

    assert len(scores) % 2 == 1
    scores.sort()

    return scores[len(scores)//2]


def test_A0():
    with open('data0') as fp:
        assert 26397 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA0():
    with open('data0') as fp:
        assert 288957 == main2(fp)

def test_BB():
    with open('data') as fp:
        print(main2(fp))
