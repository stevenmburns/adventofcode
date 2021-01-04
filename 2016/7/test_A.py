import pytest
import io
import re
import hashlib

def parse(fp):
    seq = []
    p = re.compile(r'^[a-z]+(\[[a-z]+\][a-z]+)*$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line

        lst = line.replace(']',' ').replace('[',' ').split(' ')

        seq.append(lst)

        assert len(lst) % 2 == 1

    return seq

def is_abba( s):
    for i in range(len(s)-3):
        w = s[i:i+4]
        if w[0] != w[1] and w[0] == w[3] and w[1] == w[2]:
            return True
    return False

def aba_data( s, ss):
    for i in range(len(s)-2):
        w = s[i:i+3]
        if w[0] != w[1] and w[0] == w[2]:
            ss.add( (w[0],w[1]))
    return ss

def bab_data( s, ss):
    for i in range(len(s)-2):
        w = s[i:i+3]
        if w[0] != w[1] and w[0] == w[2] and (w[1],w[0]) in ss:
            return True
    return False

def main(fp):
    seq = parse(fp)

    count = 0
    for lst in seq:
        found_good = False
        found_bad = False
        for (idx,w) in enumerate(lst):
            v = is_abba(w)
            if idx % 2 == 0 and v:
                found_good = True
            if idx % 2 == 1 and v:
                found_bad = True
        if found_good and not found_bad:
            count += 1

    return count

def main2(fp):
    seq = parse(fp)

    count = 0
    for lst in seq:

        ss = set()
        for (idx,w) in enumerate(lst):
            if idx % 2 == 0:
                ss = aba_data(w, ss)
        found_bab = False
        for (idx,w) in enumerate(lst):
            if idx % 2 == 1:
                if bab_data( w, ss):
                    found_bab = True
        if found_bab:
            count += 1

    return count

def test_abba():
    assert is_abba( 'abba')
    assert is_abba( 'abbax')
    assert is_abba( 'xabba')
    assert is_abba( 'xabbax')

def test_A():
    with open('data0', 'rt') as fp:
        assert 2 == main(fp)
    with open('data1', 'rt') as fp:
        assert 3 == main2(fp)


def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))
    with open('data', 'rt') as fp:
        print(main2(fp))
