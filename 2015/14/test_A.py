import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import json

import sys

logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p = re.compile( r'^(\S+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line
        seq.append( (m.groups()[0], int(m.groups()[1]), int(m.groups()[2]), int(m.groups()[3])))

    return seq

class Reindeer:
    def __init__(self, nm, speed, flight_time, rest_time):
        self.nm = nm
        self.speed = speed
        self.flight_time = flight_time
        self.rest_time = rest_time
 
    @property
    def cycle_time(self):
        return self.flight_time + self.rest_time

    def distance_travelled(self,time):
        quotient, remainder = divmod( time, self.cycle_time)
        return self.speed*(quotient*self.flight_time + min(remainder,self.flight_time))

def main(fp,time=1000):
    seq = parse(fp)
    reindeers = [ Reindeer( *tup) for tup in seq]
    
    return max( r.distance_travelled(time) for r in reindeers)

def main2(fp,time=1000):
    seq = parse(fp)
    reindeers = [ Reindeer( *tup) for tup in seq]
    
    scores = [ 0 for _ in reindeers]
    for t in range(1,time+1):
        best_score,best_idx = max( (r.distance_travelled(t),idx) for idx,r in enumerate(reindeers))
        scores[best_idx] += 1

    return max(scores)

#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 1120 == main(fp,time=1000)

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp,time=2503))

#@pytest.mark.skip
def test_AA0():
    with open("data0", "rt") as fp:
        assert 689 == main2(fp,time=1000)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp,time=2503))

