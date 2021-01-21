import sys
import pytest
import io
import re
import itertools
from collections import deque

class Symbol:
    def __init__(self,nm):
        self.nm = nm
    def __repr__(self):
        return self.nm

def parse(fp):
    seq = []
    p2 = re.compile(r'^(\S+) (\S+)$') 
    p3 = re.compile(r'^(\S+) (\S+) (\S+)$') 
    p_int = re.compile(r'^((|-)\d+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p2.match(line)
        if m:
            seq.append( m.groups())
            continue
        m = p3.match(line)
        if m:
            seq.append( m.groups())
            continue
        assert False, line

    new_seq = []
    for tup in seq:
        lst = [tup[0]]
        for x in tup[1:]:
            m = p_int.match(x)
            if m:
                lst.append( int(x))
            else:
                lst.append( Symbol(x))
        new_seq.append( tuple(lst))

    return new_seq

def sim(seq):

    tbl = {}
    def get_value( a):
        if type(a) == Symbol:
            if a.nm in tbl:
                return tbl[a.nm]
            else:
                return 0
        else:
            return a

    def set_value( a, value):
        tbl[a.nm] = value

    multiplies = 0
    pc = 0

    while 0 <= pc < len(seq):
        tup = seq[pc]
        if tup[0] == 'set':
            set_value( tup[1], get_value(tup[2]))
        elif tup[0] == 'add':
            set_value( tup[1], get_value(tup[1]) + get_value(tup[2]))
        elif tup[0] == 'sub':
            set_value( tup[1], get_value(tup[1]) - get_value(tup[2]))
        elif tup[0] == 'mul':
            set_value( tup[1], get_value(tup[1]) * get_value(tup[2]))
            multiplies += 1
        elif tup[0] == 'mod':
            set_value( tup[1], get_value(tup[1]) % get_value(tup[2]))
        elif tup[0] == 'jnz':
            cond = get_value(tup[1])
            if cond != 0:
                pc += get_value(tup[2]) - 1
        else:
            assert False, tup
        pc += 1

    return multiplies

def sim2(seq):

    tbl = { 'a' : 1}
    def get_value( a):
        if type(a) == Symbol:
            if a.nm in tbl:
                return tbl[a.nm]
            else:
                return 0
        else:
            return a

    def set_value( a, value):
        tbl[a.nm] = value

    multiplies = 0
    pc = 0

    count = 0

    while 0 <= pc < len(seq):
        if count % 100000 == 0:
            print(count, pc, tbl.get('h'))

        tup = seq[pc]
        if tup[0] == 'set':
            set_value( tup[1], get_value(tup[2]))
        elif tup[0] == 'add':
            set_value( tup[1], get_value(tup[1]) + get_value(tup[2]))
        elif tup[0] == 'sub':
            set_value( tup[1], get_value(tup[1]) - get_value(tup[2]))
        elif tup[0] == 'mul':
            set_value( tup[1], get_value(tup[1]) * get_value(tup[2]))
            multiplies += 1
        elif tup[0] == 'mod':
            set_value( tup[1], get_value(tup[1]) % get_value(tup[2]))
        elif tup[0] == 'jnz':
            cond = get_value(tup[1])
            if cond != 0:
                pc += get_value(tup[2]) - 1
        else:
            assert False, tup
        pc += 1
        count += 1

    return tbl['h']

def main(fp):
    seq = parse(fp)
    return sim(seq)

def main2(fp):
    seq = parse(fp)
    return sim2(seq)


"""
def disasm():
    b = 79
    c = b
    if a != 0: jump E
    jump D
E:  b *= 100         
    b -= -100000     
    c = b            
    c -= -17000      
D:  f = 1            
    d = 2
A:  e = 2
B:  g = d
    g *= e
    g -= b
    if g != 0: jump C
    f = 0
C:  e -= -1
    g = e
    g -= b
    if g != 0: jump B
    d -= -1
    g = d
    g -= b
    if g != 0: jump A
    if f != 0: jump G
    h -= -1
G:  g = b
    g -= c
    if g != 0: jump F
    jump exit
F:  b -= -17
    jump D
"""    

"""
def disasm():
    b = 107900         
    c = 124900
while True:
    f = 1            
    d = 2
    while True:
        e = 2
        while True:
            if d * e == b:
                f = 0
            e += 1
            if e == b: break
        d += 1
        if d == b: break

    if f == 0:
        h += 1
    if b == c: exit
    b += 17
"""    

"""
def disasm():
    b = 107900         
    c = 124900
while True:
    f = is b prime?
    if f == 0:
        h += 1
    if b == c: exit
    b += 17


"""    

import math


def primes_between( a, b, s):
    def is_prime(x):
        M = int(math.sqrt(x)+2)
        assert (M-1)**2 >= x
        for f in range(2, M):
            if x % f == 0:
                return False
        print(x, 'prime', M)
        return True
    count = 0
    for x in range(a,b+1, s):
        if not is_prime(x):
            count += 1 
    return count

def test_A():
    with open("data","rt") as fp:
        print(main(fp))

def test_AA():
    print(primes_between( 107900, 124900, 17))



