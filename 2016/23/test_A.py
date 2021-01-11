import pytest
import io
import re

class Register:
    def __init__(self, nm):
        self.nm = nm
    def __repr__(self):
        return f'Register({self.nm})'

def parse(fp):

    p2 = re.compile(r'^(\S+) (\S+)$')
    p3 = re.compile(r'^(\S+) (\S+) (\S+)$')

    seq = []

    def build(s):
        if s in ["a","b","c","d"]:
            return Register(s)
        else:
            return int(s)

    for line in fp:
        line = line.rstrip('\n')

        m = p2.match(line)
        if m:
            cmd = m.groups()[0]
            op1 = build(m.groups()[1])
            seq.append( (cmd,op1))
            continue
        m = p3.match(line)
        if m:
            cmd = m.groups()[0]
            op1 = build(m.groups()[1])
            op2 = build(m.groups()[2])
            seq.append( (cmd,op1,op2))
            continue
        assert False, line

    return seq

def sim(seq,registers):


    def get_value(o):
        if type(o) is Register:
            return registers[o.nm]
        else:
            return o

    pc = 0
    while 0 <= pc < len(seq):
        tup = seq[pc]
        if tup[0] == 'cpy':
            if type(tup[2]) is Register:
                registers[tup[2].nm] = get_value(tup[1])
        elif tup[0] == 'inc':
            assert type(tup[1]) is Register
            registers[tup[1].nm] += 1
        elif tup[0] == 'dec':
            assert type(tup[1]) is Register
            registers[tup[1].nm] -= 1
        elif tup[0] == 'jnz':
            u = get_value(tup[1])
            v = get_value(tup[2])
            if u != 0:
                pc += v
                continue
        elif tup[0] == 'tgl':
            tgl_inst = pc + get_value(tup[1])

            if 0 <= tgl_inst < len(seq):
                tgl_tup = seq[tgl_inst]

                if len(tgl_tup) == 2:
                    if tgl_tup[0] == 'inc':
                        new_cmd = 'dec'
                    else:
                        new_cmd = 'inc'
                    seq[tgl_inst] = (new_cmd, tgl_tup[1])
                else:
                    if tgl_tup[0] == 'jnz':
                        new_cmd = 'cpy'
                    else:
                        new_cmd = 'jnz'
                    seq[tgl_inst] = (new_cmd, tgl_tup[1], tgl_tup[2])
        else:
            assert False, tup
        pc += 1

    return registers['a']

def main(fp):
    seq = parse(fp)
    registers = {'a':7, 'b':0, 'c':0, 'd':0}
    return sim(seq,registers)

def main2(fp):
    def factorial( n):
        return n*factorial(n-1) if n > 1 else 1


    seq = parse(fp)
    for i in range(6,10):
        registers = {'a':i, 'b':0, 'c':0, 'd':0}
        print( sim(seq[:],registers)-factorial(i))

    return 6853+factorial(12)

def test_A():
    with open('data0', 'rt') as fp:
        assert 3 == main(fp)

def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))

