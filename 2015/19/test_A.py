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

def parse(fp):
    seq = []

    p = re.compile(r'^(\S+) => (\S+)$')
    p_blank = re.compile(r'^$')

    s = None
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        if m:
            seq.append( m.groups())
            continue
        m = p_blank.match(line)
        if m:
            continue
        assert s is None
        s = line

    return seq, s


def str2lst(s):
    i = 0
    r = []
    while i < len(s):
        if i+1 < len(s) and s[i+1].islower():
            r.append( s[i:i+2])
            i += 2
        else:
            r.append( s[i:i+1])
            i += 1                
    return r

def main(fp):
    seq, s = parse(fp)

    l = str2lst(s)

    tbl = defaultdict(list)
    for p,q in seq:
        tbl[p].append(str2lst(q))

    new_molecules = set()
    for i in range(len(l)):
        prefix = l[:i]
        suffix = l[i+1:]
        k = l[i]
        logging.info( f'{l} "{prefix}" "{k}" "{suffix}" {i}')
        assert l == prefix + [k] + suffix
        if k in tbl:
            for mid in tbl[k]:
                ss = prefix + mid + suffix
                logging.info(ss)
                new_molecules.add( tuple(ss))

    return len(new_molecules)

def main2(fp):
    seq, s = parse(fp)

    translate_tbl = { 'Rn': '(', 'Y': ',', 'Ar': ')'}

    l = str2lst(s)

    tbl = defaultdict(list)
    for p,q in seq:
        tbl[p].append(str2lst(q))

    print( l)
    print(tbl)


    l = [ translate_tbl.get( x, x) for x in l]

    new_tbl = {}
    for p,vv in tbl.items():
        print(f'SMB: {vv}')
        new_tbl[p] = [[ translate_tbl.get( x, x) for x in v] for v in vv]

    tbl = new_tbl
    print(tbl)

    lhs_symbols = set( tbl.keys())
    rhs_symbols = { x for vv in tbl.values() for v in vv for x in v}

    all_symbols = lhs_symbols.union(rhs_symbols)

    print(f'all_symbols {all_symbols}')

    nonterminals = set(tbl.keys())
    terminals = all_symbols.difference( nonterminals)
    print(f'terms {terminals}')
    print(f'nonterms {nonterminals}')
    print(tbl)

    for p,vv in tbl.items():
        for v in vv:
            print( f'{p} -> {" ".join(v)}')

    print( ' '.join(l))

    histo = defaultdict(int)
    for c in l:
        histo[c] += 1

    comma_count = histo[',']
    lparen_count = histo['(']
    rparen_count = histo[')']

    print( lparen_count, rparen_count, comma_count, len(l))

    return len(l) - lparen_count - rparen_count - 2*comma_count - 1


    level = 0
    for c in l:
        if c == ')':
            level -= 1
        if c == ',':
            level -= 1
        print( ' '*4*level, c)
        if c == '(':
            level += 1
        if c == ',':
            level += 1

    def gen_next(l):
        new_molecules = set()
        for i in range(len(l)):
            prefix = l[:i]
            suffix = l[i+1:]
            k = l[i]
            logging.info( f'{l} "{prefix}" "{k}" "{suffix}" {i}')
            assert l == prefix + (k,) + suffix
            if k in tbl:
                for mid in tbl[k]:
                    ss = prefix + tuple(mid) + suffix
                    logging.info(ss)
                    new_molecules.add( tuple(ss))
        return new_molecules

    reached = set()
    frontier = { ('e',) }
    level = 0
    while frontier:
        skip = 0
        print( f'level {level} reached {len(reached)} frontier {len(frontier)}')
        new_frontier = set()
        
        for s in frontier:
            for ss in gen_next(s):
                if ss == tuple(l):
                    return level + 1
                if len(ss) > len(l):
                    skip += 1
                    continue

                new_frontier.add(ss)
        print( f'skip {skip}')

        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)
        level += 1

    return None

@pytest.mark.skip
def test_A0():
    with open("data0", "rt") as fp:
        assert 4 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print(main(fp))

@pytest.mark.skip
def test_AA1():
    with open("data1", "rt") as fp:
        assert 3 == main2(fp)

@pytest.mark.skip
def test_AA2():
    with open("data2", "rt") as fp:
        assert 6 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data", "rt") as fp:
        print(main2(fp))
