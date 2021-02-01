import pytest
import io
import re
import itertools
from collections import defaultdict,deque

def parse(fp):

    seq = []
    p = re.compile(r'^Step (\S+) must be finished before step (\S+) can begin\.$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( (m.groups()[0], m.groups()[1]))

    return seq

import heapq

def main(fp):
    seq = parse(fp)

    f_edges = {}
    
    nodes = set()
    for (u,v) in seq:
        nodes.add(u)
        nodes.add(v)

    be_count = {}

    for u in nodes:
        f_edges[u] = []
        be_count[u] = 0

    for (u,v) in seq:
        f_edges[u].append(v)
        be_count[v] += 1

    q = []
    for v in nodes:
        if be_count[v] == 0:
            heapq.heappush( q, v)

    result = []
    while q:
        print(q)
        u = heapq.heappop(q)
        result.append(u)
        for v in f_edges[u]:
            be_count[v] -= 1
            if be_count[v] == 0:
                heapq.heappush(q,v)

    return ''.join(result)

def main2(fp,*,delay,workers):
    seq = parse(fp)

    f_edges = {}
    
    nodes = set()
    for (u,v) in seq:
        nodes.add(u)
        nodes.add(v)

    be_count = {}

    for u in nodes:
        f_edges[u] = []
        be_count[u] = 0

    for (u,v) in seq:
        f_edges[u].append(v)
        be_count[v] += 1

    stall_queue = []
    q = []

    def transfer(time):
        def d(u):
            return delay+ord(u)-ord('A')+1
        for _ in range(min(len(stall_queue),workers-len(q))):
            _,u = heapq.heappop(stall_queue)
            heapq.heappush(q,(time+d(u),u))

    time=0
    for v in nodes:
        if be_count[v] == 0:
            heapq.heappush( stall_queue, (time,v))
    transfer(time)

    while q:
        print(q,stall_queue)
        time = q[0][0]
        while q and time == q[0][0]:
            ts,u = heapq.heappop(q)
            for v in f_edges[u]:
                be_count[v] -= 1
                if be_count[v] == 0:
                    heapq.heappush(stall_queue,(time,v))
        transfer(time)

    return time

@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 'CABDFE' == main(fp)
 
@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA():
    with open('data0', 'rt') as fp:
        assert 15 == main2(fp,delay=0,workers=2)

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp,delay=60,workers=5))
