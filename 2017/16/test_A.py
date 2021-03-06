import sys
import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append( line.split(','))
    assert len(seq) == 1

    p_s = re.compile(r'^s(\d+)$')
    p_x = re.compile(r'^x(\d+)/(\d+)$')
    p_p = re.compile(r'^p([a-z])/([a-z])$')

    result = []
    for txt in seq[0]:
        m = p_s.match(txt)
        if m:
            result.append( ('s', int(m.groups()[0])))
            continue
        m = p_x.match(txt)
        if m:
            result.append( ('x', int(m.groups()[0]), int(m.groups()[1])))
            continue
        m = p_p.match(txt)
        if m:
            result.append( ('p', m.groups()[0], m.groups()[1]))
            continue
        assert False, txt

    return result

def dance( n, seq, a):
    for cmd in seq:
        if cmd[0] == 's':
            i = (-cmd[1]) % n 
            a = a[i:] + a[:i]
        elif cmd[0] == 'x':
            i,j = cmd[1], cmd[2]
            a[i], a[j] = a[j], a[i]
        elif cmd[0] == 'p':
            i,j = a.index(cmd[1]), a.index(cmd[2])
            a[i], a[j] = a[j], a[i]
    return a

def dance0( n, seq, a):
    for cmd in seq:
        if cmd[0] == 's':
            i = (-cmd[1]) % n 
            a = a[i:] + a[:i]
        elif cmd[0] == 'x':
            i,j = cmd[1], cmd[2]
            a[i], a[j] = a[j], a[i]
    return a

def dance1( n, seq, a):
    for cmd in seq:
        if cmd[0] == 'p':
            i,j = a.index(cmd[1]), a.index(cmd[2])
            a[i], a[j] = a[j], a[i]
    return a

def main(fp,n,repeat=1):
    seq = parse(fp)

    a = [ chr(ord('a')+x) for x in range(n)]

    for _ in range(repeat):
        a = dance(n,seq,a)

    result = a[:]

    if True:
        a = [ chr(ord('a')+x) for x in range(n)]

        for _ in range(repeat):
            a = dance0(n,seq,a)

        for _ in range(repeat):
            a = dance1(n,seq,a)

        result2 = a[:]

        assert result == result2

    return ''.join(result)

def find_cycles( s):
    ss = [ ord(c) - ord('a') for c in s]
    found = set()
    cycles = []
    for i in range(len(s)):
        if i not in found:
            found.add(i)
            cycles.append( [i])
            j = ss[i]
            while j != i:
                assert j not in found
                found.add(j)
                cycles[-1].append( j)
                j = ss[j]

    return [ ''.join(chr(x+ord('a')) for x in cycle) for cycle in cycles]

def test_find_cycles():
    assert [ 'ab', 'c'] == find_cycles( 'bac')

def test_find_cycles():
    assert ['akbpmendohl','cfji','g'] == find_cycles( 'kpfonjglcibaedhm')

def main2(fp,n):

    seq = parse(fp)

    a = [ chr(ord('a')+x) for x in range(n)]

    dance_results = []
    reached = set()
    def add(a):
        aa = tuple(a)
        if aa in reached:
            return True
        reached.add(aa)
        dance_results.append(aa)
        return False

    add(a)
    for _ in range(1000000):
        a = dance( n,seq,a)
        if add(a):
            break

    assert len(reached) == len(dance_results)
    
    print( len(dance_results))

    k = 1000*1000*1000
    q = k % len(dance_results)

    return ''.join( dance_results[q])

def compute_repeat(cycles, s, k=1000000000):
    result = ''
    for idx,c in enumerate(s):
        for cycle in cycles:
            if c in cycle:
                i = cycle.index(c)
                j = (i+k) % len(cycle)
                result += cycle[j]
        assert len(result) == idx+1
    return ''.join( result)

def main2alt(fp,n):

    seq = parse(fp)
    s = ''.join(chr(ord('a')+x) for x in range(n))

    a0 = dance0( n, seq, list(s))
    cycles0 = find_cycles( a0)
    a1 = dance1( n, seq, list(s))
    cycles1 = find_cycles( a1)

    return compute_repeat( cycles1, compute_repeat( cycles0, s))

@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 'baedc' == main(fp,5)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print( main(fp,16))

@pytest.mark.skip
def test_B0():
    with open("data","rt") as fp:
        print( main(fp,16,repeat=100))

def test_BB():
    with open("data","rt") as fp:
        print(main2(fp,16))

def test_C():
    with open("data","rt") as fp:
        print(main2alt(fp,16))
