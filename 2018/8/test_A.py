import pytest
import io
import re
import itertools
from collections import defaultdict

def parse(fp):

    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( line)

    assert len(seq) == 1

    return [ int(x) for x in seq[0].split(' ')]

def main(fp):
    seq = parse(fp)
    print(seq)

    sum = 0

    def aux( root,level):
        nonlocal sum
        print('aux',root,level)
        assert 0 <= root < len(seq) 
        assert root+1 < len(seq) 
        child_nodes = seq[root]
        metadata_entries = seq[root+1]
        child = root+2
        for _ in range(child_nodes):
            child = aux(child,level+1)
        for idx in range(child,child+metadata_entries):
            sum += seq[idx]
        return child + metadata_entries

    assert aux(0,0) == len(seq)

    return sum

def mainalt(fp):
    seq = parse(fp)

    def aux( root,level):
        print('aux',root,level)
        assert 0 <= root < len(seq) 
        assert root+1 < len(seq) 
        child_nodes = seq[root]
        metadata_entries = seq[root+1]
        child = root+2
        ss = 0
        for _ in range(child_nodes):
            child,s = aux(child,level+1)
            ss += s
        for idx in range(child,child+metadata_entries):
            ss += seq[idx]
        return child + metadata_entries, ss

    cursor, ss = aux(0,0)
    assert cursor == len(seq)
    return ss

def main2(fp):
    seq = parse(fp)

    def aux( root,level):
        print('aux',root,level)
        assert 0 <= root < len(seq) 
        assert root+1 < len(seq) 
        child_nodes = seq[root]
        metadata_entries = seq[root+1]
        child = root+2
        ss = 0
        if child_nodes == 0:
            for idx in range(child,child+metadata_entries):
                ss += seq[idx]
        else:
            values = []
            for _ in range(child_nodes):
                child,s = aux(child,level+1)
                values.append(s)
            for idx in range(child,child+metadata_entries):
                metadata = seq[idx]-1
                if 0 <= metadata < len(values):
                    ss += values[metadata]
        return child + metadata_entries, ss

    cursor, ss = aux(0,0)
    assert cursor == len(seq)
    return ss

@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 138 == main(fp)
 
@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA():
    with open('data0', 'rt') as fp:
        assert 66 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))
