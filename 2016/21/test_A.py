import pytest
import io
import re
import hashlib
from collections import deque

def parse(fp):
    seq = []
    p_rotate = re.compile(r'^rotate (right|left) (\d+) step(|s)$')
    p_swap_letter = re.compile(r'^swap letter (\S) with letter (\S)$')
    p_swap_position = re.compile(r'^swap position (\d+) with position (\d+)$')
    p_reverse_positions = re.compile(r'^reverse positions (\d+) through (\d+)$')
    p_move_position = re.compile(r'^move position (\d+) to position (\d+)$')
    p_rotate_letter = re.compile(r'^rotate based on position of letter (\S)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p_rotate.match(line)
        if m:
            cmd = "rotate " + m.groups()[0]
            arg = int(m.groups()[1])
            seq.append( (cmd,arg))
            continue
        m = p_swap_letter.match(line)
        if m:
            cmd = "swap letter"
            args = (m.groups()[0], m.groups()[1])
            seq.append( (cmd,args))
            continue
        m = p_swap_position.match(line)
        if m:
            cmd = "swap position"
            args = (int(m.groups()[0]), int(m.groups()[1]))
            seq.append( (cmd,args))
            continue
        m = p_reverse_positions.match(line)
        if m:
            cmd = "reverse positions"
            args = (int(m.groups()[0]), int(m.groups()[1]))
            seq.append( (cmd,args))
            continue
        m = p_move_position.match(line)
        if m:
            cmd = "move position"
            args = (int(m.groups()[0]), int(m.groups()[1]))
            seq.append( (cmd,args))
            continue
        m = p_rotate_letter.match(line)
        if m:
            cmd = "rotate letter"
            arg = m.groups()[0]
            seq.append( (cmd,arg))
            continue
        assert False, line

    return seq

def step( cmd, args, a):
    save_a = a[:]
    save_len = len(a)
    if cmd == "rotate right":
        a = a[-args:] + a[:-args]
    elif cmd == "rotate left":
        a = a[args:] + a[:args]
    elif cmd == "swap letter":
        xs = [ idx for idx in range(len(a)) if a[idx] == args[0]]
        ys = [ idx for idx in range(len(a)) if a[idx] == args[1]]
        for idx in xs:
            a[idx] = args[1]
        for idx in ys:
            a[idx] = args[0]
    elif cmd == "swap position":
        a[args[0]], a[args[1]] = a[args[1]], a[args[0]]
    elif cmd == "rotate letter":
        xs = [ idx for idx in range(len(a)) if a[idx] == args]
        assert len(xs) > 0
        rot = xs[0]
        if rot >= 4:
            rot += 1
        rot += 1
        rot %= len(a)
        a = a[-rot:] + a[:-rot]
    elif cmd == "move position":
        x = a[args[0]]
        a = a[:args[0]] + a[args[0]+1:]
        a = a[:args[1]] + [x] + a[args[1]:]
    elif cmd == "reverse positions":
        foo = a[args[0]:args[1]+1]
        a[args[0]:args[1]+1] = foo[::-1]
    else:
        assert False, (cmd,args)
    assert len(a) == save_len, (cmd,args)

    return a

from itertools import permutations

def invstep( cmd, args, a):
    count = 0
    for aa in permutations(a):
        lstaa = list(aa)
        if step(cmd, args, lstaa) == a:
            print( cmd, args, ''.join(lstaa), ''.join(a), count)
            return lstaa
        count += 1
    assert False, (cmd, args, a)

def sim( seq, txt):
    a = list(txt)

    for (cmd, args) in seq:
        a = step( cmd, args, a)

    return ''.join(a)

def invsim( seq, txt):
    a = list(txt)

    for (cmd, args) in reversed(seq):
        a = invstep( cmd, args, a)

    result = ''.join(a)

    assert sim(seq, result) == txt

    return result

def invsim( seq, txt):
    
    for txt0_tuple in permutations(txt):
        txt0 = ''.join(txt0_tuple)
        if sim(seq, txt0) == txt:
            return txt0
    assert False, (cmd, args, txt)

def main(fp, txt):
    seq = parse(fp)
    return sim(seq, txt)

def main2(fp, txt):
    seq = parse(fp)
    return invsim(seq, txt)

@pytest.mark.skip
def test_A():
    with open("data0", "rt") as fp:
        assert 'decab' == main(fp, 'abcde')

@pytest.mark.skip
def test_B():
    with open("data", "rt") as fp:
        print( main(fp, 'abcdefgh'))

def test_BB0():
    with open("data", "rt") as fp:
        print( main(fp, 'aghfcdeb'))

def test_BB():
    with open("data", "rt") as fp:
        print( main2(fp, 'fbgdceah'))
