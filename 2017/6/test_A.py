import pytest
import io
import re
import itertools

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append( [int(x) for x in line.split('\t')])
    assert len(seq) == 1
    return seq[0]

def redistribute( tup):
    lst = list(tup)
    n = len(lst)
    cursor = lst.index(max(lst))
    k = lst[cursor]
    lst[cursor] = 0
    for _ in range(k):
        cursor = (cursor+1) % n
        lst[cursor] += 1

    return tuple(lst)


def main(fp):
    seq = parse(fp)
    print(seq)

    state = tuple(seq)
    reached = { state}
    
    count = 0
    while True:
        count += 1
        state = redistribute(state)
        if state in reached:
            return count
        else:
            reached.add(state)

def main2(fp):
    seq = parse(fp)
    print(seq)

    state = tuple(seq)
    reached = { state : 0}
    
    count = 0
    while True:
        count += 1
        state = redistribute(state)
        print(count,state)
        if state in reached:
            return count - reached[state]
        else:
            reached[state] = count

def test_A():
    with open("data0", "rt") as fp:
        assert 5 == main(fp)

def test_AA():
    with open("data0", "rt") as fp:
        assert 4 == main2(fp)


def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))


