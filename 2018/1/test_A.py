import pytest
import io
import re
import itertools

def parse(fp):

    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append(int(line))

    return seq

def main(fp):
    return sum(parse(fp))

def main2(fp):
    reached = set()
    sum = 0
    reached.add(sum)
    seq = parse(fp)
    for x in itertools.cycle(seq):
        sum += x
        if sum in reached:
            return sum
        reached.add(sum)
    return None

#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

def test_AA0():
    txt = """+1
-1"""
    with io.StringIO(txt) as fp:
        assert 0 == main2(fp)

def test_AA1():
    txt = """+3
+3
+4
-2
-4"""
    with io.StringIO(txt) as fp:
        assert 10 == main2(fp)


#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))

