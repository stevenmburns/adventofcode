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
        assert 0 <= a < 6
        assert 0 <= b < 6
        assert 0 <= c < 6
        after[c] = before[a] + before[b]
    elif code == 'addi':
        assert 0 <= a < 6
        assert 0 <= c < 6
        after[c] = before[a] + b
    elif code == 'mulr':
        assert 0 <= a < 6
        assert 0 <= b < 6
        assert 0 <= c < 6
        after[c] = before[a] * before[b]
    elif code == 'muli':
        assert 0 <= a < 6
        assert 0 <= c < 6
        after[c] = before[a] * b
    elif code == 'banr':
        assert 0 <= a < 6
        assert 0 <= b < 6
        assert 0 <= c < 6
        after[c] = before[a] & before[b]
    elif code == 'bani':
        assert 0 <= a < 6
        assert 0 <= c < 6
        after[c] = before[a] & b
    elif code == 'borr':
        assert 0 <= a < 6
        assert 0 <= b < 6
        assert 0 <= c < 6
        after[c] = before[a] | before[b]
    elif code == 'bori':
        assert 0 <= a < 6
        assert 0 <= c < 6
        after[c] = before[a] | b
    elif code == 'setr':
        assert 0 <= a < 6
        assert 0 <= c < 6
        after[c] = before[a]
    elif code == 'seti':
        assert 0 <= c < 6
        after[c] = a
    elif code == 'gtir':
        assert 0 <= b < 6
        assert 0 <= c < 6
        after[c] = 1 if a > before[b] else 0
    elif code == 'gtri':
        assert 0 <= a < 6
        assert 0 <= c < 6
        after[c] = 1 if before[a] > b else 0
    elif code == 'gtrr':
        assert 0 <= a < 6
        assert 0 <= b < 6
        assert 0 <= c < 6
        after[c] = 1 if before[a] > before[b] else 0
    elif code == 'eqir':
        assert 0 <= b < 6
        assert 0 <= c < 6
        after[c] = 1 if a == before[b] else 0
    elif code == 'eqri':
        assert 0 <= a < 6
        assert 0 <= c < 6
        after[c] = 1 if before[a] == b else 0
    elif code == 'eqrr':
        assert 0 <= a < 6
        assert 0 <= b < 6
        assert 0 <= c < 6
        after[c] = 1 if before[a] == before[b] else 0

    return after
    

def parse(fp):
    seq = []

    p_cmd = re.compile(r'^(\S+) (\d+) (\d+) (\d+)$')
    p_ip = re.compile(r'^\#ip (\d+)$')

    ip_num = None

    for line in fp:
        line = line.rstrip('\n')
        m = p_cmd.match(line)
        if m:
            assert ip_num is not None

            seq.append( (m.groups()[0], int(m.groups()[1]), int(m.groups()[2]), int(m.groups()[3])))

            continue

        m = p_ip.match(line)
        if m:
            assert ip_num is None
            assert len(seq) == 0
            ip_num = int(m.groups()[0])
            continue

        assert False, line


    return seq, ip_num

def sim( seq, ip_num, r0_start, part2):
    ip = 0

    state = { i : 0 for i in range(6)}

    state[0] = r0_start

    #print( ip, state)

    histo = defaultdict(int)

    r5_values = set()
    last_r5_value = None

    count = 0
    while 0 <= ip < len(seq):
        histo[ip] += 1

        if count % 1000 == 0:
            pass
            #print( [ (k,v) for k,v in histo.items()])

        op, a, b, c = seq[ip]

        state[ip_num] = ip

        state = step( op, a, b, c, state)
        if ip == 29:
            r5 = state[5]
            if not part2:
                return r5
            if state[5] in r5_values:
                if part2:
                    return last_r5_value
            last_r5_value = r5
            r5_values.add(r5)
            print(r5)                

        ip = state[ip_num]
        ip += 1
        #print(ip,state)
        count += 1

    return state[0]

def main(fp,r0_start=0,part2=False):
    seq, ip_num = parse(fp)
    return sim( seq, ip_num, r0_start, part2)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp,r0_start=0,part2=False))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main(fp,r0_start=0,part2=True))
