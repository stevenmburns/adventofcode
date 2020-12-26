
import io
import pytest

import logging
from logging import debug
import re

def parse(fp):
    

    rules = []

    my_ticket = None
    nearby_tickets = []

    p_rule = re.compile(r"^(.+): (\d+)\-(\d+) or (\d+)\-(\d+)$")
    p_blank = re.compile(r"^$")
    p_tag1 = re.compile(r"^your ticket:$")
    p_tag2 = re.compile(r"^nearby tickets:$")

    state = 'rules'

    for line in fp:
        line = line.rstrip('\n')
        if state == 'rules':
            if p_blank.match(line):
                state = 'tag1'
            else:
                m = p_rule.match(line)
                assert m, line
                rules.append( (m.groups()[0],
                               ((int(m.groups()[1]),int(m.groups()[2])),
                                (int(m.groups()[3]),int(m.groups()[4])))))
        elif state == 'tag1':
            m = p_tag1.match(line)
            assert m
            state = 'my_ticket'
        elif state == 'tag2':
            m = p_tag2.match(line)
            assert m
            state = 'nearby_tickets'
        elif state == 'my_ticket':
            if p_blank.match(line):
                state = 'tag2'
            else:
                assert my_ticket is None
                my_ticket = [ int(x) for x in line.split(',')]
        elif state == 'nearby_tickets':
            nearby_tickets.append( [ int(x) for x in line.split(',')])

    assert my_ticket is not None

    return (rules, my_ticket, nearby_tickets)

def main( fp):
    (rules, my_ticket, nearby_tickets) = parse(fp)

    valid_set = set()
    for nm,pair in rules:
        for (m,M) in pair:
            for i in range(m,M+1):
                valid_set.add(i)

    scanning_error_rate = 0
    for ticket in nearby_tickets:
        failures = 0
        for value in ticket:
            if value in valid_set:
                pass
            else:
                failures += 1
                scanning_error_rate += value
        assert failures in [0,1]

    return scanning_error_rate

def main2( fp):
    (rules, my_ticket, nearby_tickets) = parse(fp)

    valid_set = set()
    for nm,pair in rules:
        for (m,M) in pair:
            for i in range(m,M+1):
                valid_set.add(i)

    valid_tickets = []
    for ticket in nearby_tickets:
        failures = 0
        for value in ticket:
            if value in valid_set:
                pass
            else:
                failures += 1

        if failures == 0:
            valid_tickets.append(ticket)

    possible_fields = {}
    for nm,pair in rules:
        for (m,M) in pair:
            for i in range(m,M+1):
                if i not in possible_fields:
                    possible_fields[i] = set()
                possible_fields[i].add(nm)

    result = []
    n = len(valid_tickets[0])
    for i in range(n):
        s = possible_fields[valid_tickets[0][i]]
        for ticket in valid_tickets[1:]:
            s = s.intersection(possible_fields[ticket[i]])
        result.append(s)

    while True:
        known = set()
        for s in result:
            assert len(s) > 0
            if len(s) == 1:
                known.add(list(s)[0])
        changed = False
        new_result = []
        for s in result:        
            if len(s) == 1:
                new_result.append(s)
            else:
                if s.intersection(known):
                    changed = True
                new_result.append( s.difference(known))
        result = new_result
        if not changed:
            break

    for s in result:        
        assert len(s) == 1

    prod = 1
    for (idx,s) in enumerate(result):
        if list(s)[0].startswith( 'departure'):
            prod *= my_ticket[idx]
    return prod

def test_A():
    with open( "data0", "rt") as fp:
        assert 71 == main(fp)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))
