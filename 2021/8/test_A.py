import re
from itertools import permutations, chain
from collections import defaultdict, Counter

def parse(fp):
    p = re.compile(r'^(.*) \| (.*)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m, line

        yield m.groups()[0].split(" "), m.groups()[1].split(" ")



def main(fp):
    data = list(parse(fp))

    tbl = { 1: "cf", 4: "bcdf", 7: "acf", 8: "abcdefg"}

    lengths = set(len(s) for s in tbl.values())

    res = 0

    for a, b in data:
        for bb in b:
            if len(bb) in lengths:
                res += 1
    return res

def aux(a, b):

    tbl = { 0: "abcefg", 1: "cf", 2: "acdeg", 3: "acdfg", 
            4: "bcdf",   5: "abdfg", 6: "abdefg", 7: "acf",
            8: "abcdefg", 9: "abcdfg"}

    legal = { frozenset( list(s) ) : idx for idx, s in tbl.items() }
    segs = "abcdefg"

    legal_perms = set()

    for perm in permutations(segs):
        m = dict(zip(segs, perm))
        if all(frozenset( m[c] for c in aa ) in legal for aa in a):
            legal_perms.add(perm)

    assert len(legal_perms) == 1

    perm = list(legal_perms)[0]
    m = dict(zip(segs, perm))

    res = 0
    for bb in b:
        code = legal[frozenset( m[c] for c in bb )]
        res = res*10 + code

    return res

def main2(fp):
    data = list(parse(fp))
    return sum( aux(a, b) for a, b in data )

def main3(fp):
    data = list(parse(fp))

    tbl = { 0: "abcefg", 1: "cf", 2: "acdeg", 3: "acdfg", 
            4: "bcdf",   5: "abdfg", 6: "abdefg", 7: "acf",
            8: "abcdefg", 9: "abcdfg"}

    inv_tbl = { frozenset( v) : k for k, v in tbl.items() }

    def gen_codes(a):
        l = defaultdict(list)
        for s in a:
            l[len(s)].append(s)
        ll = {k: Counter( chain(*v)) for k, v in l.items()}
        return { c : frozenset( (k, v.get(c, 0)) for k, v in ll.items())
                for c in "abcdefg" }

    codes = gen_codes(tbl.values())
    assert len(codes) == len(set(codes.values()))
    inv_codes = { v: k for k, v in codes.items() }

    result = 0
    for a, b in data:
        new_codes = gen_codes(a)
        res = 0
        for bb in b:
            s = frozenset(inv_codes[new_codes[c]] for c in bb)
            res = 10*res + inv_tbl[s]
        result += res
    return result

def test_A0():
    with open('data0') as fp:
        assert 26 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA0():
    with open('data0') as fp:
        assert 61229 == main2(fp)

def test_AAA0():
    with open('data0') as fp:
        assert 61229 == main3(fp)

def test_BB():
    with open('data') as fp:
        print(main2(fp))

def test_BBB():
    with open('data') as fp:
        print(main3(fp))