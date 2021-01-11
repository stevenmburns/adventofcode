import pytest
import io
import re
import hashlib
from collections import deque

def parse(fp):
    seq = []
    p = re.compile(r'^(\d+)-(\d+)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( (int(m.groups()[0]),int(m.groups()[1])))

    return seq

def simplify(seq):

    seq.sort()

    new_seq = []
    lb, ub = seq[0]
    for p in seq[1:]:
        if p[0] <= ub + 1:
            ub = max(ub,p[1])
        else:
            new_seq.append( (lb,ub))
            lb, ub = p

    new_seq.append( (lb,ub))

    return new_seq

def main(fp):
    seq = parse(fp)

    new_seq = simplify(seq)
    print(new_seq)    

    if new_seq[0][0] > 0:
        return 0
    else:
        return new_seq[0][1] + 1

def main2(fp):
    seq = parse(fp)

    new_seq = simplify(seq)
    print(new_seq)    

    M = 1 << 32

    i = 0
    
    count = 0
    for (lb,ub) in new_seq:
        count += lb-i
        i = ub+1

    if i < M:
        count += M - 1 - i

    return count

def test_A():
    with open("data0", "rt") as fp:
        assert 3 == main(fp)

def test_B():
    with open("data", "rt") as fp:
        print( main(fp))
    with open("data", "rt") as fp:
        print( main2(fp))
