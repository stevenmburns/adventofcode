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

def decompress(s):
    p = re.compile(r'\s')
    p_encode = re.compile(r'^(\d+)x(\d+)$')

    m = p.match(s)
    assert not m

    new_s = ''
    i = 0
    while i < len(s):
        if s[i] == '(':
            i += 1
            ss = ''
            while s[i] != ')':
                ss += s[i]
                i += 1
            i += 1
            m = p_encode.match(ss)
            assert m, ss
            span,rep = int(m.groups()[0]), int(m.groups()[1])
            new_s += s[i:i+span] * rep
            i += span
        else:
            new_s += s[i]
            i += 1

    return new_s

def decompress2(s):
    p = re.compile(r'\s')
    p_encode = re.compile(r'^(\d+)x(\d+)$')

    m = p.match(s)
    assert not m

    new_s = ''
    i = 0
    while i < len(s):
        if s[i] == '(':
            i += 1
            ss = ''
            while s[i] != ')':
                ss += s[i]
                i += 1
            i += 1
            m = p_encode.match(ss)
            assert m, ss
            span,rep = int(m.groups()[0]), int(m.groups()[1])
            
            segment = s[i:i+span]
            
            segment = decompress2(segment)

            new_s += segment * rep
            i += span
        else:
            new_s += s[i]
            i += 1

    return new_s

def main(fp):
    seq = parse(fp)
    line = ''.join(seq)
    new_line = decompress(line)
    return len(new_line)

def main2(fp):
    seq = parse(fp)
    line = ''.join(seq)
    new_line = decompress2(line)
    return len(new_line)

def test_A():
    txt = """ADVENT
A(1x5)BC
(3x3)XYZ
A(2x2)BCD(2x2)EFG
(6x1)(1x3)A
"""
    with io.StringIO(txt) as fp:
        assert 39 == main(fp)

def test_A0():
    txt = """ADVENT
"""
    with io.StringIO(txt) as fp:
        assert 6 == main(fp)

def test_A1():
    txt = """A(1x5)BC
"""
    with io.StringIO(txt) as fp:
        assert 7 == main(fp)

def test_A2():
    txt = """(3x3)XYZ
"""
    with io.StringIO(txt) as fp:
        assert 9 == main(fp)

def test_A3():
    txt = """A(2x2)BCD(2x2)EFG
"""
    with io.StringIO(txt) as fp:
        assert 11 == main(fp)

def test_A4():
    txt = """(6x1)(1x3)A
"""
    with io.StringIO(txt) as fp:
        assert 6 == main(fp)

def test_AA0():
    txt = """(3x3)XYZ
"""
    with io.StringIO(txt) as fp:
        assert 9 == main2(fp)

def test_AA1():
    txt = """X(8x2)(3x3)ABCY
"""
    with io.StringIO(txt) as fp:
        assert 20 == main2(fp)

def test_AA2():
    txt = """(27x12)(20x12)(13x14)(7x10)(1x12)A
"""
    with io.StringIO(txt) as fp:
        assert 241920 == main2(fp)

def test_AA3():
    txt = """(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN
"""
    with io.StringIO(txt) as fp:
        assert 445 == main2(fp)

@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))
