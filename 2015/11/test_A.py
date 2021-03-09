import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO)

def password_ok(txt):
    assert len(txt) == 8

    straight = False
    for i in range(2,len(txt)):
        a,b,c = txt[i-2],txt[i-1],txt[i]
        if ord(a) + 2 == ord(b) + 1 == ord(c):
            straight = True

    bad_letter = any( c in "iol" for c in txt)

    rule3 = False
    for i in range(1,len(txt)):
        a,b = txt[i-1],txt[i]
        if a == b:
            for j in range(i+2,len(txt)):
                c,d = txt[j-1],txt[j]
                if c == d and a != c:
                    rule3 = True

    return straight and not bad_letter and rule3

def incr_txt(txt):
    new_txt = deque()
    carry = True
    for c in reversed(txt):
        if carry:
            cc = ord(c) + 1
            if cc > ord('z'):
                cc = ord('a')
                carry = True
            else:
                carry = False
            new_txt.appendleft(chr(cc))
        else:
            new_txt.appendleft( c)
    return ''.join(new_txt)

def test_incr_txt():
    assert 'aaaaaaab' == incr_txt('aaaaaaaa')
    assert 'aaaaaaba' == incr_txt('aaaaaaaz')
    assert 'aaaqaaaa' == incr_txt('aaapzzzz')

def main(txt):
    while True:
        txt = incr_txt(txt)
        if password_ok(txt):
            return txt


@pytest.mark.skip
def test_A0():
    assert not password_ok( 'hijklmmn')

@pytest.mark.skip
def test_A1():
    assert not password_ok( 'abbceffg')

@pytest.mark.skip
def test_A2():
    assert not password_ok( 'abbcegjk')

@pytest.mark.skip
def test_A3():
    assert 'abcdffaa' == main('abcdefgh')

@pytest.mark.skip
def test_A4():
    assert 'ghjaabcc' == main('ghijklmn')

@pytest.mark.skip
def test_B():
    print(main('hxbxwxba'))

#@pytest.mark.skip
def test_BB():
    print(main(main('hxbxwxba')))

