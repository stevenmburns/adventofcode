import pytest
import io
import re
import itertools

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append( line.split(' '))
    return seq

def main(fp):
    seq = parse(fp)

    count = 0
    for line in seq:
        words = set()
        found_duplicate = False
        for word in line:
            if word in words:
                found_duplicate = True
            words.add(word)
        if not found_duplicate:
            count += 1

    return count

def main2(fp):
    seq = parse(fp)

    count = 0
    for line in seq:
        sorted_words = set()
        found_duplicate = False
        for word in line:
            a = list(word)
            a.sort()
            sorted_word = ''.join(a)
            if sorted_word in sorted_words:
                found_duplicate = True
            sorted_words.add(sorted_word)
        if not found_duplicate:
            count += 1

    return count

def test_A0():
    txt = """aa bb cc dd ee
"""
    with io.StringIO(txt) as fp:
        assert 1 == main(fp)

def test_A1():
    txt = """aa bb cc dd aa
"""
    with io.StringIO(txt) as fp:
        assert 0 == main(fp)

def test_A2():
    txt = """aa bb cc dd aaa
"""
    with io.StringIO(txt) as fp:
        assert 1 == main(fp)

def test_AA0():
    txt = """abcde fghij
"""
    with io.StringIO(txt) as fp:
        assert 1 == main2(fp)

def test_AA1():
    txt = """abcde xyz ecdab
"""
    with io.StringIO(txt) as fp:
        assert 0 == main2(fp)

def test_AA2():
    txt = """a ab abc abd abf abj
"""
    with io.StringIO(txt) as fp:
        assert 1 == main2(fp)

def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))

