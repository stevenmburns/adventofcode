from os import rename
import re
from itertools import permutations, chain, product
from collections import defaultdict, Counter, deque

def parse(fp):
    for line in fp:
        line = line.rstrip('\n')
        yield line


def main(fp):
    data = parse(fp)
    m = { '{':'}', '[':']', '(':')', '<':'>' }
    im = { v: k for k, v in m.items() } 
    def aux(s):
        stack = []
        while s:
            c = s.popleft()
            if c in m:
                stack.append(c)
            elif c in im:
                if not stack:
                    return c, stack
                if im[c] != stack[-1]:
                    return c, stack
                stack.pop()
        else:
            return None, stack

    tbl = { ')' : 3, '}' : 1197, ']' : 57, '>' : 25137 }

    res = 0
    for line in data:
        s = deque(line)
        c, stack = aux(s)
        if c is not None:
            res += tbl[c]


    return res

def main2(fp):
    data = parse(fp)
    m = { '{':'}', '[':']', '(':')', '<':'>' }
    im = { v: k for k, v in m.items() } 
    def aux(s):
        stack = []
        while s:
            c = s.popleft()
            if c in m:
                stack.append(c)
            elif c in im:
                if not stack:
                    return c, stack
                if im[c] != stack[-1]:
                    return c, stack
                stack.pop()
        else:
            return None, stack

    tbl = { ')' : 1, '}' : 3, ']' : 2, '>' : 4 }

    scores = []
    for line in data:
        s = deque(line)
        c, stack = aux(s)
        if c is None:
            score = 0
            print('stack:', stack)
            while stack:
                cc = stack.pop()
                score = score*5 + tbl[m[cc]]

            scores.append(score)

    print(scores)

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
