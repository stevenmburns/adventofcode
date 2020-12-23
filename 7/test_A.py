
import io
import pytest

import logging
from logging import debug
import re

#logging.basicConfig(level=logging.DEBUG)

def count_bags( rules, leaf):
    tbl = {}
    for lhs, rhs_lst in rules:
        tbl[lhs] = []
        for rhs in rhs_lst:
            tbl[lhs].append(rhs)

    count = 0

    memo = set([leaf])
    def leads_to_leaf( u):
        nonlocal memo
        if u in memo:
            return True
        else:
            for c,v in tbl[u]:
                if leads_to_leaf( v):
                    memo.add(u)
            return u in memo

    for (k,v) in tbl.items():
        leads_to_leaf(k)

    return len(memo) - 1


def parse( fp):
    #debug("Part 1")

    p = re.compile(r"^(\S+) (\S+) bag(|s) contain(( (\d+) (\S+) (\S+) bag(|s)(,|.))+)$")
    p_none = re.compile(r"^(\S+) (\S+) bag(|s) contain no other bags.+$")
    p_sub = re.compile(r"^ (\d+) (\S+) (\S+) bag(|s)$")


    rules = []

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        if m:
            lhs = (m.groups()[0],m.groups()[1])
            rhs_str = m.groups()[3]
            q = rhs_str[:-1].split(',')
            rhs = []
            for str in q:
                mm = p_sub.match(str)
                assert mm, str
                rhs.append( (int(mm.groups()[0]), (mm.groups()[1], mm.groups()[2])))
            rules.append( (lhs, rhs))
        else:
            m = p_none.match(line)            
            if m:
                lhs = (m.groups()[0],m.groups()[1])
                rules.append( (lhs, []))
            else:
                assert False, line
    return rules

def main( fp):
    rules = parse(fp)
    return count_bags( rules, ('shiny', 'gold'))

def total_bags( rules, container):
    tbl = {}
    for lhs, rhs_lst in rules:
        tbl[lhs] = []
        for rhs in rhs_lst:
            tbl[lhs].append(rhs)

    memo = {}
    def aux( u):
        nonlocal memo
        if u in memo:
            return memo[u]
        else:
            count = 1
            for c,v in tbl[u]:
                subcount = aux( v)
                count += c*subcount
                    
            memo[u] = count
            return count

    return aux( container) - 1


def main2( fp):
    rules = parse(fp)
    return total_bags( rules, ('shiny', 'gold'))

def test_A():
    txt = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""
    with io.StringIO(txt) as fp:
        assert 4 == main(fp)
    with io.StringIO(txt) as fp:
        assert 32 == main2(fp)

def test_B():
    txt = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""
    with io.StringIO(txt) as fp:
        assert 126 == main2(fp)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))
