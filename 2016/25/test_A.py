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
    emitted = []

    while 0 <= pc < len(seq) and len(emitted) < 20:
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
        elif tup[0] == 'out':
            emitted.append(get_value(tup[1]))
        else:
            assert False, tup
        pc += 1


    return emitted

def main(fp):
    seq = parse(fp)
    signal = [0,1]*10

    for i in range(1000):
        registers = {'a':i, 'b':0, 'c':0, 'd':0}
        emitted = sim(seq,registers)
        print( i, emitted, signal)
        if emitted == signal:
            return i
    return None

def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

