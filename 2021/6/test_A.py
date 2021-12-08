
import re
from itertools import combinations, product
from collections import defaultdict, Counter

def parse(fp):
    for line in fp:
        line = line.rstrip('\n')
        yield from [int(x) for x in line.split(',')]


def main(fp):
    ages = list(parse(fp))

    for _ in range(80):
        new_ages = []
        new_fish = 0
        for a in ages:
            if a == 0:
                new_ages.append(6)
                new_fish += 1
            else:
                new_ages.append(a - 1)
        new_ages.extend([8] * new_fish)
        ages = new_ages
    return len(ages)

def main2(fp):

    histo = Counter(parse(fp))

    for _ in range(256):
        new_histo = Counter()
        for a, v in histo.items():
            if a == 0:
                new_histo[6] += v
                new_histo[8] += v
            else:
                new_histo[a-1] += v
        histo = new_histo
    return sum(histo.values())

def main3(fp):

    histo = Counter(parse(fp))

    c = [6703087164, 6206821033, 5617089148, 5217223242, 4726100874,
        4368232009, 3989468462, 3649885552, 3369186778]
    return sum(c[k]*v for k,v in histo.items())

def test_A0():
    with open('data0') as fp:
        assert 5934 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA0():
    with open('data0') as fp:
        assert 26984457539 == main2(fp)

def test_BB():
    with open('data') as fp:
        print(main2(fp))

def test_BBB():
    with open('data') as fp:
        print(main3(fp))