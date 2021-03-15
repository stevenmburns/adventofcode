import hashlib
import pytest
import io
import re
import itertools
from functools import reduce
from collections import defaultdict, deque
import logging
import json

import sys

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append(int(line))

    return seq

def gen_subsets_with_sum( s, k):

    subsets = set()
    def aux( tup, remaining, k):
        #print( tup, remaining, k)
        assert set(tup).union(set(remaining)) == set(s)

        if k == 0:
            subsets.add( frozenset(tup))
            return

        for idx,x in enumerate(remaining):
            prefix = remaining[:idx]
            suffix = remaining[idx+1:]
            new_remaining = tuple(prefix) + tuple(suffix)
            if x <= k:
                aux( tup + [x], new_remaining, k-x)

        
    aux( [], s, k)
    return subsets

def test_gen_subsets_with_sum():
    print(gen_subsets_with_sum( [1,2,3], 4))


def gen_subsets( s):
    for k in range(0,len(s)+1):
        for comb in itertools.combinations( s, k):
            yield comb

def gen_subsets_with_sum_simple( seq, k):
    for s in gen_subsets(seq):
        if sum(s) == k:
            yield s

def main(fp):
    seq = parse(fp)

    total_weight = sum(seq)

    assert total_weight % 3 == 0

    bin_weight = total_weight // 3

    def qe(s):
        return reduce( lambda a,b: a*b, s)

    best = None
    for s0 in gen_subsets_with_sum_simple( seq, bin_weight):
        if best is not None and len(s0) > best[0]:
            break
        ss = set(seq).difference(set(s0))
        for s1 in gen_subsets_with_sum_simple( list(ss), bin_weight):
            cand = (len(s0),qe(s0))
            if best is None or best > cand:
                best = cand
            break

    return best[1]

def main2(fp):
    seq = parse(fp)

    total_weight = sum(seq)

    assert total_weight % 4 == 0

    bin_weight = total_weight // 4

    def qe(s):
        return reduce( lambda a,b: a*b, s)

    best = None
    for s0 in gen_subsets_with_sum_simple( seq, bin_weight):
        if best is not None and len(s0) > best[0]:
            break
        ss = set(seq).difference(set(s0))

        for s1 in gen_subsets_with_sum_simple( list(ss), bin_weight):
            sss = ss.difference(set(s1))
            found = False
            for s2 in gen_subsets_with_sum_simple( list(sss), bin_weight):
                cand = (len(s0),qe(s0))
                if best is None or best > cand:
                    best = cand
                found = True
                break
            if found:
                break

    return best[1]

@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 99 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open("data0", "rt") as fp:
        assert 44 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))
