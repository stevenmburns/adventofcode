import hashlib
import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO)

def parse(fp):

    p_copy_op = re.compile( r'^(\S+) -> (\S+)$')
    p_binary_op = re.compile( r'^(\S+) (AND|OR|LSHIFT|RSHIFT) (\S+) -> (\S+)$')
    p_unary_op = re.compile( r'^(NOT) (\S+) -> (\S+)$')

    seq = []
    for line in fp:
        line = line.rstrip('\n')
        m = p_copy_op.match(line)
        if m:
            seq.append( ('COPY', m.groups()[0], m.groups()[1]))
        m = p_binary_op.match(line)
        if m:
            seq.append( (m.groups()[1], m.groups()[0], m.groups()[2], m.groups()[3]))
        m = p_unary_op.match(line)
        if m:
            seq.append( (m.groups()[0], m.groups()[1], m.groups()[2]))

    return seq


def main(fp,final='a',override_b=None):

    seq = parse(fp)

    def to_int( s):
        p_int = re.compile( r'^(\d+)$')
        if p_int.match(s):
            return int(s)
        else:
            return s

    new_seq = []
    for tup in seq:
        if tup[0] in ['COPY','NOT']:
            new_seq.append( (tup[0], to_int(tup[1]), tup[2]))
        else:
            new_seq.append( (tup[0], to_int(tup[1]), to_int(tup[2]), tup[3]))

    succ = {}
    gate = {}
    pred_counts = {}
    for tup in new_seq:
        for j in range(1, len(tup)):
            succ[tup[j]] = []
            pred_counts[tup[j]] = 0

    for idx,tup in enumerate(new_seq):
        gate[tup[-1]] = idx
        for j in range(1,len(tup)-1):
            succ[tup[j]].append( tup[-1])
            pred_counts[tup[-1]] += 1

    for k, v in pred_counts.items():
        if v == 0:
            assert type(k) != str

    q = deque()
    for k, v in pred_counts.items():
        if v == 0:
            q.appendleft( k)

    topoorder = []
    while q:
        u = q.pop()
        topoorder.append(u)
        for v in succ[u]:
            pred_counts[v] -= 1
            if pred_counts[v] == 0:
                q.appendleft( v)

    print(topoorder)

    overrides = {}
    if override_b is not None:
        overrides['b'] = override_b


    v_tbl = {}
    def g(s):
        if type(s) == str:
            if s in overrides:
                return overrides[s]
            else:
                return v_tbl[s]
        else:
            return s

    for v in topoorder:
        if type(v) == str:
            idx = gate[v]
            tup = new_seq[idx]
            if tup[0] == 'COPY':
                v_tbl[v] = g(tup[1])
            elif tup[0] == 'NOT':
                v_tbl[v] = ~g(tup[1])
            elif tup[0] == 'AND':
                v_tbl[v] = g(tup[1]) & g(tup[2])
            elif tup[0] == 'OR':
                v_tbl[v] = g(tup[1]) | g(tup[2])
            elif tup[0] == 'LSHIFT':
                v_tbl[v] = g(tup[1]) << g(tup[2])
            elif tup[0] == 'RSHIFT':
                v_tbl[v] = g(tup[1]) >> g(tup[2])

    print(v_tbl)

    return v_tbl[final] % (1<<16)


#@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 65079 == main(fp,final='i')

#@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp,final='a'))

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main(fp,final='a',override_b=46065))


