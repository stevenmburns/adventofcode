import pytest
import io
import re
import hashlib
from collections import deque

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)
    assert len(seq) == 1
    return seq[0]
               
def main(fp,nrows):
    row = parse(fp)

    def nextrow(row):
        result = ''
        for i in range(len(row)):
            l = row[i-1] if i-1>=0 else '.'
            c = row[i]
            r = row[i+1] if i+1<len(row) else '.'
            if l == '^' and c == '^' and r == '.' or \
               l == '.' and c == '^' and r == '^' or \
               l == '^' and c == '.' and r == '.' or \
               l == '.' and c == '.' and r == '^':
                result += '^'
            else:
                result += '.'
        return result

    count = sum( 1 for c in row if c == '.')
    for _ in range(nrows-1):
        row_next = nextrow(row)
        count += sum( 1 for c in row_next if c == '.')
        row = row_next

    return count

def test_A0():
    with open('data0','rt') as fp:
        assert 6 == main(fp,3)

def test_A1():
    with open('data1','rt') as fp:
        assert 38 == main(fp,10)

def test_B():
    with open('data','rt') as fp:
        print( main(fp,40))

def test_B0():
    with open('data','rt') as fp:
        print( main(fp,400000))
