import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import json

import sys

#logging.basicConfig(level=logging.INFO)


def step( attacker, defender):
    (hp0,damage0,armor0) = attacker
    (hp1,damage1,armor1) = defender
    return hp1 - max(damage0 - armor1, 1), damage1, armor1


def play( me, boss):
    print( me, boss)
    while True:
        boss = step( me, boss)
        print( me, boss)
        if boss[0] <= 0:
            return True
        me = step( boss, me)
        print( me, boss)
        if me[0] <= 0:
            return False


def test_play():
    assert play( (8,5,5), (12,7,2))



def main():

    weapons_costs = [(8,4,0),(10,5,0),(25,6,0),(40,7,0),(74,8,0)]
    armor_costs = [(0,0,0),(13,0,1),(31,0,2),(53,0,3),(75,0,4),(75,0,4),(102,0,5)]
    ring_costs = [(25,1,0),(50,2,0),(100,3,0),(20,0,1),(40,0,2),(80,0,3)]

    best = None
    for w in weapons_costs:
        for a in armor_costs:
            for rs in itertools.chain( itertools.combinations( ring_costs, 0),
                                       itertools.combinations( ring_costs, 1),
                                       itertools.combinations( ring_costs, 2)):
                tup = (w,) + (a,) + rs
                cost = sum( triple[0] for triple in tup)
                damage = sum( triple[1] for triple in tup)
                armor = sum( triple[2] for triple in tup)

                me = (100,damage,armor)
                boss = (104,8,1)

                if play( me, boss):
                    if best is None or cost < best: best = cost

    return best

def main2():

    weapons_costs = [(8,4,0),(10,5,0),(25,6,0),(40,7,0),(74,8,0)]
    armor_costs = [(0,0,0),(13,0,1),(31,0,2),(53,0,3),(75,0,4),(75,0,4),(102,0,5)]
    ring_costs = [(25,1,0),(50,2,0),(100,3,0),(20,0,1),(40,0,2),(80,0,3)]

    best = None
    for w in weapons_costs:
        for a in armor_costs:
            for rs in itertools.chain( itertools.combinations( ring_costs, 0),
                                       itertools.combinations( ring_costs, 1),
                                       itertools.combinations( ring_costs, 2)):
                tup = (w,) + (a,) + rs
                cost = sum( triple[0] for triple in tup)
                damage = sum( triple[1] for triple in tup)
                armor = sum( triple[2] for triple in tup)

                me = (100,damage,armor)
                boss = (104,8,1)

                if not play( me, boss):
                    if best is None or cost > best: best = cost

    return best

#@pytest.mark.skip
def test_B():
    print(main())

#@pytest.mark.skip
def test_BB():
    print(main2())

