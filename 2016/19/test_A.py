import pytest
import io
import re
import hashlib
from collections import deque

def main(n):

    next = [None] + [ (i % n) + 1 for i in range(1,n+1)]
    presents = [None] + [ 1 for i in range(1,n+1)]

    cursor = 1

    while next[cursor] != cursor:
        presents[cursor] += presents[next[cursor]]
        presents[next[cursor]] = 0
        next[cursor] = next[next[cursor]]
        cursor = next[cursor]

    return cursor

def main2(n):

    next = [None] + [ (i % n) + 1 for i in range(1,n+1)]
    presents = [None] + [ 1 for i in range(1,n+1)]

    cursor = 1
    prev_cursor2 = (n-1)//2

    count = n

    while next[cursor] != cursor:
        presents[cursor] += presents[next[prev_cursor2]]
        next[prev_cursor2] = next[next[prev_cursor2]]
        cursor = next[cursor]
        if count % 2 == 1: # advance prev_cursor2
            prev_cursor2 = next[prev_cursor2]
        count -= 1

    return cursor

def test_A():
    assert 3 == main(5)
    assert 2 == main2(5)

def test_B():
    print( main(3014387))
    print( main2(3014387))
