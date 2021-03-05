import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import heapq

logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p_new = re.compile(r'^deal into new stack$')
    p_cut = re.compile(r'^cut ((|-)\d+)$')
    p_incr = re.compile(r'^deal with increment (\d+)$')

    for line in fp:
        line = line.rstrip('\n')

        m = p_new.match(line)
        if m:
            seq.append( ('new',))
            continue

        m = p_cut.match(line)
        if m:
            seq.append( ('cut', int(m.groups()[0])))
            continue

        m = p_incr.match(line)
        if m:
            seq.append( ('incr', int(m.groups()[0])))
            continue
        seq.append( line)

    return seq

def exe( deck, cmd):
    if cmd[0] == 'new':
        new_deck = deck[:]
        new_deck.reverse()
        return new_deck
    elif cmd[0] == 'cut':
        k = cmd[1]
        new_deck = deck[k:] + deck[:k]
        return new_deck
    elif cmd[0] == 'incr':
        k = cmd[1]
        assert 1 == extended_euclid( k, len(deck))[0]

        new_deck = [None]*len(deck)
        i = 0
        for x in deck:
            new_deck[i] = x
            i = (i + k) % len(deck)

        return new_deck
    else:
        assert False, cmd

def extended_euclid( a, b):
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_euclid( b%a, a)
    return d, y1 - (b // a) * x1, x1

def inv_mod( a, m):
    gcd, x, y = extended_euclid( a, m)
    assert gcd == 1
    return x % m

def test_extended_euclid():
    assert 7 == inv_mod( 3, 10)
    assert 1 == (3*inv_mod(3,10)) % 10


def gen_mat( f):
    p, q, m = f
    """
    q -p
    0 1
"""

def hit( f, x):
    p, q, m = f
    return (p + q*x)%m

def compose( g, f):
    p, q, m = f
    u, v, m2 = g
    assert m == m2
    return (u+v*p)%m, (v*q)%m, m

def invert( f):
    # invf( f( i)) == i for all i

    p, q, m = f

    """
    0 = (u+v*p)%m
    1 = (v*q)%m
"""

    v = inv_mod( q, m)
    u = (-v*p) % m

    return u, v, m

def power_compose( f, n):
    p, q, m = f
    y = 0, 1, m
    while n > 0:
        if n % 2 == 0:
            f = compose( f, f)
            n = n // 2
        else:
            y = compose( f, y)
            n = n - 1
    return y

def check_power_compose( f, n):
    p, q, m = f
    y = 0, 1, m
    for _ in range(n):
        y = compose( y, f)

    assert y == power_compose( f, n)

def test_power_compose():
    check_power_compose( (1,1,10), 1001)
    check_power_compose( (2,1,10), 1001)
    check_power_compose( (2,3,10), 1001)
    check_power_compose( (2,3,10), 8)

def check_invert( *f):
    h = compose( invert( f), f)
    p, q, m = h
    assert p == 0 and q == 1

    assert all( hit(h,i) == i for i in range(f[2]))

def test_invert():
    check_invert( 4, 7, 10)
    check_invert( 0, 1, 10)
    check_invert( 1, 1, 10)
    check_invert( 1, 9, 10)
    check_invert( -1, 9, 10)


def get_f( m, cmd):
    if cmd[0] == 'new':
        return ( m-1, -1, m)
    elif cmd[0] == 'cut':
        k = cmd[1]
        return ( -k, 1, m)
    elif cmd[0] == 'incr':
        k = cmd[1]
        return (0, k, m)
    else:
        assert False, cmd

def exe2( f, cmd):
    _, _, m = f
    g = get_f( m, cmd)
    return compose( g, f)

#@pytest.mark.skip
def test_new():
    deck = list(range(10))

    deck = exe(deck, ('new',))

    assert '9876543210' == ''.join( str(x) for x in deck)

#@pytest.mark.skip
def test_cut():
    deck = list(range(10))

    deck = exe(deck, ('cut',2))

    assert '2345678901' == ''.join( str(x) for x in deck)

#@pytest.mark.skip
def test_cut_minus():
    deck = list(range(10))

    deck = exe(deck, ('cut',-2))

    assert '8901234567' == ''.join( str(x) for x in deck)

#@pytest.mark.skip
def test_incr():
    deck = list(range(10))
    deck = exe(deck, ('incr',3))

    assert '0741852963' == ''.join( str(x) for x in deck)

#@pytest.mark.skip
def test_new2():
    deck = 0, 1, 10

    deck = exe2(deck, ('new',))

    u, v, m = deck
    assert '9876543210' == ''.join( str(hit(deck,x)) for x in range(m))

#@pytest.mark.skip
def test_cut2():
    deck = 0, 1, 10

    deck = exe2(deck, ('cut',2))
    deck = invert(deck)

    u, v, m = deck
    assert '2345678901' == ''.join( str(hit(deck,x)) for x in range(m))

#@pytest.mark.skip
def test_cut_minus2():
    deck = 0, 1, 10

    deck = exe2(deck, ('cut',-2))
    deck = invert(deck)

    u, v, m = deck
    assert '8901234567' == ''.join( str(hit(deck,x)) for x in range(m))

#@pytest.mark.skip
def test_incr2():
    deck = 0, 1, 5

    deck = exe2(deck, ('incr',3))
    deck = invert(deck)

    """
    01234
    02413
"""
    u, v, m = deck
    assert '02413' == ''.join( str(hit(deck,x)) for x in range(m))

#@pytest.mark.skip
def test_increments2():

    for i in [1,3,7,9]:

        deck1 = list(range(10))
        deck1 = exe(deck1, ('incr',i))

        deck = 0, 1, 10
        deck = exe2(deck, ('incr',i))
        deck = invert(deck)
 
        u, v, m = deck
        assert deck1 == [hit(deck,x) for x in range(m)]


#@pytest.mark.skip
def test_pairs():

    m = 5

    lst = [ ('cut',1), ('incr',2)]

    """
    01234
    12340
    p,q = 1,1

    01234
    03142
    p,q = 0,3

    01234
    31420
    p,q = 3,3
=========
    01234
    12340

    14203
    p,q = 1,3
"""

    assert (3,3,5) == compose( (0,3,5), (1,1,5))

    deck1 = list(range(m))
    for idx,cmd in enumerate(lst):
        deck1 = exe(deck1, cmd)

    f = 0, 1, m
    for idx,cmd in enumerate(lst):
        f = exe2( f, cmd)

    f = invert(f)

    deck2 = [hit( f, x) for x in range(m)]
    print( deck1, deck2)
    assert deck1 == deck2


import itertools

def main_simple(fp,m,pos=2019,n=1):
    seq = parse(fp)

    deck = list(range(m))
    for cmd in seq*n:
        deck = exe( deck, cmd)

    if m == 10:
        return ''.join( str(x) for x in deck)
    else:
        return deck.index(pos)

def main_fast(fp,m,pos=2019,n=1):
    seq = parse(fp)

    f = 0, 1, m
    for cmd in seq:
        f = exe2( f, cmd)

    f = power_compose(f, n)

    if m == 10:
        f = invert(f)
        return ''.join( str(hit(f,x)) for x in range(m))
    else:
        if m > 10007:
            f = invert(f)            
        return hit( f, pos)

main = main_fast

#@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert '0369258147' == main(fp,10)

#@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert '3074185296' == main(fp,10)

#@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        assert '6307418529' == main(fp,10)

#@pytest.mark.skip
def test_A3():
    with open("data3","rt") as fp:
        assert '9258147036' == main(fp,10)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp,10007,n=1))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main_fast(fp,m=119315717514047,pos=2020,n=101741582076661))
