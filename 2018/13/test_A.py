import pytest
import io
import re
import itertools
from collections import defaultdict

def parse(fp):
    p_init = re.compile(r'^initial state: ((#|\.)+)\s*$')
    p_blank = re.compile('^\s*$')
    p_rule = re.compile(r'^((#|\.)+)\s+=>\s+((\#|\.)+)\s*$')

    initial_state = None
    rules = []

    for line in fp:
        line = line.rstrip('\n')
        m = p_init.match(line)
        if m:
            initial_state = m.groups()[0]
            continue
        m = p_blank.match(line)
        if m:
            continue
        m = p_rule.match(line)
        if m:
            rules.append( (m.groups()[0], m.groups()[2]))
            continue
        assert False, line

    return initial_state, rules


def main(fp):
    initial_state, rules = parse(fp)

    line = defaultdict(lambda: '.')

    for idx,c in enumerate(initial_state):
        if c == '#':
            line[idx] = c

    def extent( line):
        m, M = None, None
        for k,v in line.items():
            if v == '.': continue
            if m is None or k < m: m = k
            if M is None or k > M: M = k
        return m, M

    def pline( line,m,M):
        result = ''
        for idx in range(m,M+1):
            result += line[idx]
        print( result)

    pad = 4

    def step(line,m,M):
        newline = defaultdict(lambda: '.')
        for idx in range(m-pad,M+pad-5+1+1):
            for lhs, rhs in rules:
                assert len(lhs) == 5
                match = True
                for i,c in enumerate(lhs):
                    if line[idx+i] != c:
                        match = False
                if match:
                    assert len(rhs) == 1
                    newline[idx+2] = rhs
        return newline

    def count(line):
        count = 0
        for k,v in line.items():
            if v == '#':
                count += k
        return count

    m, M = extent(line)
    pline(line,m,M)
    for _ in range(20):
        line = step(line,m,M)
        m,M = extent(line)
        pline(line,m,M)

    return count(line)


def extent( line):
    m, M = None, None
    for k,v in line.items():
        if v == '.': continue
        if m is None or k < m: m = k
        if M is None or k > M: M = k
    return m, M

def pline( line,m,M):
    result = ''
    for idx in range(m,M+1):
        result += line[idx]
    print( result)

def count(line):
    count = 0
    for k,v in line.items():
        if v == '#':
            count += k
    return count

def step(rules,line,m,M):
    pad = 4

    newline = defaultdict(lambda: '.')
    for idx in range(m-pad,M+pad-5+1+1):
        for lhs, rhs in rules:
            assert len(lhs) == 5
            match = True
            for i,c in enumerate(lhs):
                if line[idx+i] != c:
                    match = False
            if match:
                assert len(rhs) == 1
                newline[idx+2] = rhs
    return newline


def check(initial_state,rules,n):

    line = defaultdict(lambda: '.')

    for idx,c in enumerate(initial_state):
        if c == '#':
            line[idx] = c

    m, M = extent(line)
    for _ in range(n):
        line = step(rules,line,m,M)
        m, M = extent(line)

    return count(line)

def main2(fp):
    initial_state, rules = parse(fp)

    line = defaultdict(lambda: '.')

    for idx,c in enumerate(initial_state):
        if c == '#':
            line[idx] = c


    def freeze(line,m):
        s = set()
        for k,v in line.items():
            if v == '#':
                s.add(k-m)
        return frozenset(s)

    def counton(line):
        count = 0
        for k,v in line.items():
            if v == '#':
                count += 1
        return count

    states = {}

    m, M = extent(line)
    pline(line,m,M)

    states[freeze(line,m)] = (0,count(line))

    linear_fit = None

    for i in range(1,2001):
        line = step(rules,line,m,M)
        m,M = extent(line)
        print(i,m,M,' ',end='')
        pline(line,m,M)
        s = freeze(line,m)
        score = count(line)
        if s in states:
            linear_fit = [ states[s], (i,score)]
            break
        else:
            states[s] = (i,score)

    print(linear_fit)

    """
    y - y0 = (y1-y0)/(x1-x0) (x - x0)
"""
    (x0,y0),(x1,y1) = tuple(linear_fit)
    x = 50*1000*1000*1000
    #x = 200
    m = (y1-y0)//(x1-x0)
    print( f'm: {m} counton: {counton(line)}')
    y = y0 + m*(x-x0)

    if x < 1000:
        assert check( initial_state, rules, x) == y



    return y

def test_A():
    with open("data0","rt") as fp:
        assert 325 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main2(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))
