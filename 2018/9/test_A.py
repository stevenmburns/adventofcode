import pytest
import io
import re
import itertools
from collections import defaultdict

class Ring:
    def __init__(self):
        self.prev = [0]
        self.next = [0]
        self.cursor = 0

    def advance(self):
        self.cursor = self.next[self.cursor]

    def backup(self):
        self.cursor = self.prev[self.cursor]

    def addDummy(self):
        assert len(self.prev) == len(self.next)
        self.prev.append(None)
        self.next.append(None)

    def addAfterCursor(self):
        """
        a <-> b
==>
        a <-> x <-> b
"""
        x = len(self.prev)
        assert x == len(self.next)

        a, b = self.cursor, self.next[self.cursor]

        self.prev.append(a)
        self.next.append(b)

        self.next[a],self.prev[b] =  x, x

    def removeAtCursor(self):
        """
        a <-> x <-> b
==>
        a <-> b
"""
        a, b = self.prev[self.cursor], self.next[self.cursor]
        self.next[a],self.prev[b] =  b, a
        self.cursor = b

    def toList(self,start=None):
        if start is None:
            start = self.cursor

        result = [start]
        x = start
        while start != self.next[x]:
            x = self.next[x]
            result.append(x)

        return result

    def toReverseList(self):
        result = [self.cursor]
        x = self.cursor
        while self.cursor != self.prev[x]:
            x = self.prev[x]
            result.append(x)

        return result

def main(players,last):

    r = Ring()

    scores = defaultdict(int)

    for i in range(1,last+1):
        player = (i-1) % players + 1
        if i % 23 == 0:
            r.addDummy()
            scores[player] += i
            for _ in range(7):
                r.backup()
            scores[player] += r.cursor
            r.removeAtCursor()
        else:
            r.advance()
            r.addAfterCursor()
            r.advance()
            #print(player,r.toList(0), r.cursor)

    print(scores)
    return max(scores.values())

#@pytest.mark.skip
def test_ring():
    r = Ring()
    for i in range(10):
        r.addAfterCursor()
        r.advance()
    print(r.toList())
    print(r.toReverseList())
    r.removeAtCursor()
    print(r.toList())
    print(r.toReverseList())

def test_A():
    assert 32 == main(9,25)

#@pytest.mark.skip
def test_A0():
    assert 8317 == main(10,1618)

#@pytest.mark.skip
def test_A1():
    assert 146373 == main(13,7999)

#@pytest.mark.skip
def test_A2():
    assert 2764 == main(17,1104)

#@pytest.mark.skip
def test_A3():
    assert 54718 == main(21,6111)

#@pytest.mark.skip
def test_A4():
    assert 37305 == main(30,5807)
 
#@pytest.mark.skip
def test_B():
    print(main(429,70901))

#@pytest.mark.skip
def test_BB():
    print(main(429,70901*100))
