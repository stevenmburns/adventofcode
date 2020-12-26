
import io
import pytest

import logging
from logging import debug
import re

import re
import collections

# Token specification
pats = []
pats.append( r'(?P<LPAREN>\()')
pats.append( r'(?P<RPAREN>\))')
pats.append( r'(?P<PLUS>\+)')
pats.append( r'(?P<TIMES>\*)')
pats.append( r'(?P<NUM>\d+)')
pats.append( r'(?P<WS>\s+)')

master_pat = re.compile('|'.join(pats))

# Tokenizer
Token = collections.namedtuple('Token', ['type','value'])

def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append( list(generate_tokens(line)))

    return seq

from itertools import product

def evaluate( lst):

    last_token = None

# E -> P (OP P)+
# P -> '(' E ')' | NUM

    def have_type( ty):
        nonlocal last_token
        nonlocal lst
        if len(lst) > 0 and lst[0].type == ty:
            last_token = lst[0]
            lst = lst[1:]
            return True
        return False

    def primary():
        if have_type('LPAREN'):
            result = expr()
            assert have_type('RPAREN')
            return result
        else:
            assert have_type('NUM')
            return int(last_token.value)

    def expr():
        lhs = primary()

        while True:
            if have_type('TIMES'):
                lhs *= primary()
            elif have_type('PLUS'):
                lhs += primary()
            else:
                break

        return lhs
            
    return expr()

def evaluate2( lst):

    last_token = None

# E -> T ('*' T)+
# T -> P ('+' P)+
# P -> '(' E ')' | NUM

    def have_type( ty):
        nonlocal last_token
        nonlocal lst
        if len(lst) > 0 and lst[0].type == ty:
            last_token = lst[0]
            lst = lst[1:]
            return True
        return False

    def primary():
        if have_type('LPAREN'):
            result = expr()
            assert have_type('RPAREN')
            return result
        else:
            assert have_type('NUM')
            return int(last_token.value)

    def term():
        lhs = primary()
        while have_type('PLUS'):
            lhs += primary()
        return lhs

    def expr():
        lhs = term()
        while have_type('TIMES'):
            lhs *= term()
        return lhs
            
    return expr()




def main( fp):
    seq = parse(fp)
    return sum( evaluate(lst) for lst in seq)

def main2( fp):
    seq = parse(fp)
    return sum( evaluate2(lst) for lst in seq)


def test_A():
    with open( "data0", "rt") as fp:
        assert 71 == main(fp)
    with open( "data0", "rt") as fp:
        assert 231 == main2(fp)

def test_C():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))
