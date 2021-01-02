
import io
import pytest

import logging
from logging import debug
import re

import re
import collections
from collections import deque

def parse(fp):

    p_blank = re.compile(r'^$')
    p_card = re.compile(r'^(\d+)$')
    p_tag = re.compile(r'^Player (\d+):$')

    tbl = {}
    player = None
    for line in fp:
        line = line.rstrip('\n')
        m = p_blank.match(line)
        if m: continue
        m = p_tag.match(line)        
        if m:
            player = int(m.groups()[0])
            tbl[player] = []
            continue
        m = p_card.match(line)        
        if m:
            tbl[player].append( int(m.groups()[0]))
            continue
        assert False

    return tbl

def compute_score(deck):
    score = 0
    for i in range(0,len(deck)):
        c = deck.pop()
        score += (i+1)*c
    assert len(deck) == 0
    return score

def sim(tbl):
    deck1 = collections.deque(tbl[1])
    deck2 = collections.deque(tbl[2])

    count = len(deck1) + len(deck2)

    while len(deck1) > 0 and len(deck2) > 0:
        c1 = deck1.popleft()
        c2 = deck2.popleft()
        if c1 > c2:
            deck1.append(c1)
            deck1.append(c2)
        elif c1 < c2:
            deck2.append(c2)
            deck2.append(c1)
        else:
            assert False

    assert len(deck1) == 0 or len(deck2) == 0
    assert len(deck1) + len(deck2) == count
        
    return deck1, deck2

def aux(deck1, deck2, level=0):
    previous_states = { (tuple(deck1),tuple(deck2))}

    while len(deck1) > 0 and len(deck2) > 0:
        c1 = deck1.popleft()
        c2 = deck2.popleft()

        if c1 <= len(deck1) and c2 <= len(deck2):
            result = aux( deque(list(deck1)[:c1]), deque(list(deck2)[:c2]), level+1)
            if result == 1:
                deck1.append(c1)
                deck1.append(c2)
            else:
                deck2.append(c2)
                deck2.append(c1)
        elif c1 > c2:
            deck1.append(c1)
            deck1.append(c2)
        elif c1 < c2:
            deck2.append(c2)
            deck2.append(c1)
        else:
            assert False

        state = (tuple(deck1),tuple(deck2))
        if state in previous_states:
            return 1
        
        previous_states.add(state)

    assert len(deck1) == 0 or len(deck2) == 0

    return 1 if len(deck1) > 0 else 2


def sim2(tbl):
    deck1 = collections.deque(tbl[1])
    deck2 = collections.deque(tbl[2])

    count = len(deck1) + len(deck2)

    while len(deck1) > 0 and len(deck2) > 0:
        c1 = deck1.popleft()
        c2 = deck2.popleft()
        if c1 <= len(deck1) and c2 <= len(deck2):
            result = aux( deque(list(deck1)[:c1]), deque(list(deck2)[:c2]))
            if result == 1:
                deck1.append(c1)
                deck1.append(c2)
            else:
                deck2.append(c2)
                deck2.append(c1)
        elif c1 > c2:
            deck1.append(c1)
            deck1.append(c2)
        elif c1 < c2:
            deck2.append(c2)
            deck2.append(c1)
        else:
            assert False


    assert len(deck1) == 0 or len(deck2) == 0
    assert len(deck1) + len(deck2) == count
        
    return deck1, deck2


def main( fp):
    tbl = parse(fp)
    deck1, deck2 = sim(tbl)
    return compute_score(deck1 if len(deck1) > 0 else deck2)

def main2( fp):
    tbl = parse(fp)
    deck1, deck2 = sim2(tbl)
    return compute_score(deck1 if len(deck1) > 0 else deck2)

def test_A():
    with open( "data0", "rt") as fp:
        assert 306 == main(fp)
    with open( "data0", "rt") as fp:
        assert 291 == main2(fp)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))
