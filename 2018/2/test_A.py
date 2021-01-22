import pytest
import io
import re
import itertools

def parse(fp):

    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)

    return seq


def main(fp):
    seq = parse(fp)

    twos = 0
    threes = 0
    for line in seq:
        histo = {}
        for c in line:
            if c not in histo: histo[c] = 0
            histo[c] += 1

        has_two = False
        has_three = False
        for k,v in histo.items():
            if v == 2: has_two = True
            if v == 3: has_three = True
        if has_two:
            twos += 1
        if has_three:
            threes += 1

    return twos * threes


def main2(fp):
    seq = parse(fp)
    for i in range(len(seq)):
        for j in range(0,i):
            line0, line1 = seq[i], seq[j]
            count_different = 0
            for (x,y) in zip(line0,line1):
                if x != y:
                    count_different += 1
            if count_different == 1:
                result = ''
                for (x,y) in zip(line0,line1):
                    if x == y:
                        result += x
                return result

#@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 12 == main(fp)

#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))
