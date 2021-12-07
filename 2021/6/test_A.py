import re
from itertools import combinations, product
from collections import defaultdict

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
    ...

def test_A0():
    with open('data0') as fp:
        assert 5934 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def xtest_AA0():
    with open('data0') as fp:
        assert 12 == main2(fp)

def xtest_BB():
    with open('data') as fp:
        print(main2(fp))