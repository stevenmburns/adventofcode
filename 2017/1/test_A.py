import pytest
import io
import re

def parse(fp):

    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)

    assert len(seq) == 1

    return seq[0]

def main(fp):
    line = parse(fp)

    line = line + line[0]

    sum = 0
    for i in range(len(line)-1):
        pair = line[i:i+2]
        if pair[0] == pair[1]:
            sum += int(pair[0])

    return sum

def main2(fp):
    line = parse(fp)

    n = len(line)
    assert n % 2 == 0
    n2 = n//2

    sum = 0
    for i in range(n):
        pair = line[i],line[(i+n2)%n]
        if pair[0] == pair[1]:
            sum += int(pair[0])

    return sum

def test_A0():
    txt = '1122'
    with io.StringIO(txt) as fp:
        assert 3 == main(fp)

def test_A1():
    txt = '1111'
    with io.StringIO(txt) as fp:
        assert 4 == main(fp)

def test_A2():
    txt = '1234'
    with io.StringIO(txt) as fp:
        assert 0 == main(fp)

def test_A3():
    txt = '91212129'
    with io.StringIO(txt) as fp:
        assert 9 == main(fp)

def test_AA0():
    txt = '1212'
    with io.StringIO(txt) as fp:
        assert 6 == main2(fp)

def test_AA1():
    txt = '1221'
    with io.StringIO(txt) as fp:
        assert 0 == main2(fp)

def test_AA2():
    txt = '123425'
    with io.StringIO(txt) as fp:
        assert 4 == main2(fp)

def test_AA3():
    txt = '123123'
    with io.StringIO(txt) as fp:
        assert 12 == main2(fp)

def test_AA4():
    txt = '12131415'
    with io.StringIO(txt) as fp:
        assert 4 == main2(fp)

#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))

