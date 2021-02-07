import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)


def step( code, a, b, c, before):
    after = dict(before.items())
    if code == 'addr':
        assert 0 <= a < 4
        assert 0 <= b < 4
        assert 0 <= c < 4
        after[c] = before[a] + before[b]
    elif code == 'addi':
        assert 0 <= a < 4
        assert 0 <= c < 4
        after[c] = before[a] + b
    elif code == 'mulr':
        assert 0 <= a < 4
        assert 0 <= b < 4
        assert 0 <= c < 4
        after[c] = before[a] * before[b]
    elif code == 'muli':
        assert 0 <= a < 4
        assert 0 <= c < 4
        after[c] = before[a] * b
    elif code == 'banr':
        assert 0 <= a < 4
        assert 0 <= b < 4
        assert 0 <= c < 4
        after[c] = before[a] & before[b]
    elif code == 'bani':
        assert 0 <= a < 4
        assert 0 <= c < 4
        after[c] = before[a] & b
    elif code == 'borr':
        assert 0 <= a < 4
        assert 0 <= b < 4
        assert 0 <= c < 4
        after[c] = before[a] | before[b]
    elif code == 'bori':
        assert 0 <= a < 4
        assert 0 <= c < 4
        after[c] = before[a] | b
    elif code == 'setr':
        assert 0 <= a < 4
        assert 0 <= c < 4
        after[c] = before[a]
    elif code == 'seti':
        assert 0 <= c < 4
        after[c] = a
    elif code == 'gtir':
        assert 0 <= b < 4
        assert 0 <= c < 4
        after[c] = 1 if a > before[b] else 0
    elif code == 'gtri':
        assert 0 <= a < 4
        assert 0 <= c < 4
        after[c] = 1 if before[a] > b else 0
    elif code == 'gtrr':
        assert 0 <= a < 4
        assert 0 <= b < 4
        assert 0 <= c < 4
        after[c] = 1 if before[a] > before[b] else 0
    elif code == 'eqir':
        assert 0 <= b < 4
        assert 0 <= c < 4
        after[c] = 1 if a == before[b] else 0
    elif code == 'eqri':
        assert 0 <= a < 4
        assert 0 <= c < 4
        after[c] = 1 if before[a] == b else 0
    elif code == 'eqrr':
        assert 0 <= a < 4
        assert 0 <= b < 4
        assert 0 <= c < 4
        after[c] = 1 if before[a] == before[b] else 0

    return after


def check( before, cmd, after):
    opnum, a, b, c = cmd

    before_tbl = dict( zip(range(4),before))

    compatible_codes = set()
    for code in ['addr','addi',
                 'mulr','muli',
                 'banr','bani',
                 'borr','bori',
                 'setr','seti',
                 'gtir','gtri','gtrr',
                 'eqir','eqri','eqrr']:
        after_tbl = step( code, a, b, c, before_tbl)

        all_same = True
        for i in range(4):
            if after[i] != after_tbl[i]:
                all_same = False
        if all_same:
            compatible_codes.add(code)
            
    return compatible_codes

    

def parse(fp):
    seq = []
    test_seq = []

    p_before = re.compile(r'^Before:\s+\[(\d+), (\d+), (\d+), (\d+)\]$')
    p_after = re.compile(r'^After:\s+\[(\d+), (\d+), (\d+), (\d+)\]$')
    p_tuple = re.compile(r'^(\d+) (\d+) (\d+) (\d+)$')
    p_blank = re.compile(r'^$')

    before = None
    cmd = None

    for line in fp:
        line = line.rstrip('\n')
        m = p_before.match(line)
        if m:
            assert before is None
            assert cmd is None
            before = tuple( int(x) for x in m.groups())
            continue

        m = p_tuple.match(line)
        if m:
            if before is not None:
                assert cmd is None
                cmd = tuple( int(x) for x in m.groups())
            else:
                test_seq.append( tuple( int(x) for x in m.groups()))
            continue

        m = p_after.match(line)
        if m:
            assert before is not None
            assert cmd is not None

            after = tuple( int(x) for x in m.groups())
            seq.append( (before, cmd, after))
            before, cmd = None, None
            continue

        m = p_blank.match(line)
        if m:
            continue
        assert False, line
        seq.append(line)
    return seq, test_seq

def main(fp):
    seq, test_seq = parse(fp)
    print(len(seq),len(test_seq))

    count = 0
    for before, cmd, after in seq:
        if len(check( before, cmd, after)) >= 3:
            count += 1
    return count

def main2(fp):
    seq, test_seq = parse(fp)
    print(len(seq),len(test_seq))

    codes = {}

    count = 0
    for before, cmd, after in seq:
        code, _, _, _ = cmd
        compatible_codes = check( before, cmd, after)

        if code not in codes:
            codes[code] = compatible_codes
        else:
            codes[code] = codes[code].intersection(compatible_codes) 


    result = {}

    while True:
        for_sure = set()
        for k,v in codes.items():
            if len(v) == 1:
                for_sure.add(list(v)[0])
                result[k] = list(v)[0]

        for k in codes.keys():
            codes[k] = codes[k].difference(for_sure)

        print(for_sure)

        if not for_sure:
            break

    assert len(result) == 16

    print(result)

    state = { i : 0 for i in range(4)}
    for opnum, a, b, c in test_seq:
        state = step( result[opnum], a, b, c, state)

    return state[0]

@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 1 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))

