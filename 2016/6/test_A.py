import pytest
import io
import re
import hashlib

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)
    return seq

def main(fp):
    seq = parse(fp)
    
    result = ''
    for i in range(len(seq[0])):
        histo = {}
        for line in seq:
            c = line[i]
            if c not in histo:
                histo[c] = 0
            histo[c] += 1
        
        pairs = [ (-v,k) for (k,v) in histo.items()]
        pairs.sort()
        
        result += pairs[0][1]

    return result

def main2(fp):
    seq = parse(fp)
    
    result = ''
    for i in range(len(seq[0])):
        histo = {}
        for line in seq:
            c = line[i]
            if c not in histo:
                histo[c] = 0
            histo[c] += 1
        
        pairs = [ (v,k) for (k,v) in histo.items()]
        pairs.sort()
        
        result += pairs[0][1]

    return result

def test_A():
    with open('data0', 'rt') as fp:
        assert 'easter' == main(fp)


def test_B():
    with open('data', 'rt') as fp:
        print(main2(fp))
