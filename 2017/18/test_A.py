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

send_count0, send_count1 = 0, 0

def step( procnum, seq, tbl, pc, inq, outq):
    global send_count0, send_count1

    def get_value( a):
        if type(a) == Symbol:
            if a.nm not in tbl:
                tbl[a.nm] = 0
            return tbl[a.nm]
        else: 
            return a

    def set_value( a, value):
        assert type(a) == Symbol
        tbl[a.nm] = value

    tup = seq[pc]
    print(procnum,tbl,pc,inq,outq,tup,end=' ')
    if tup[0] == 'set':
        set_value( tup[1], get_value(tup[2]))
    elif tup[0] == 'add':
        set_value( tup[1], get_value(tup[1]) + get_value(tup[2]))
    elif tup[0] == 'mul':
        set_value( tup[1], get_value(tup[1]) * get_value(tup[2]))
    elif tup[0] == 'mod':
        set_value( tup[1], get_value(tup[1]) % get_value(tup[2]))
    elif tup[0] == 'jgz':
        cond = get_value(tup[1])
        if cond > 0:
            pc += get_value(tup[2]) - 1
    elif tup[0] == 'snd':
        if procnum == 0:
            send_count0 += 1
        elif procnum == 1:
            send_count1 += 1
        else:
            assert False, procnum
        outq.append( get_value(tup[1]))
    elif tup[0] == 'rcv':
        if inq:
            set_value( tup[1], inq.popleft())
        else:
            print('Stall',tbl,pc,inq,outq)
            return tbl, pc, True            
            
    else:
        assert False, tup

    pc += 1
    print(tbl,pc,inq,outq)

    return tbl, pc, False


def sim2(seq):
    tbl0, pc0 = { 'p': 0}, 0
    tbl1, pc1 = { 'p': 1}, 0
    
    q0to1, q1to0 = deque(), deque()

    while True:
        both_finished = True
        both_waiting = True
        for _ in range(1):
            if 0 <= pc0 < len(seq):
                both_finished = False
                tbl0, pc0, waiting0 = step( 0, seq, tbl0, pc0, q1to0, q0to1)
                if not waiting0:
                    both_waiting = False
        for _ in range(1):
            if 0 <= pc1 < len(seq):
                both_finished = False
                tbl1, pc1, waiting1 = step( 1, seq, tbl1, pc1, q0to1, q1to0)
                if not waiting1:
                    both_waiting = False
            
        print( f'{both_finished} {both_waiting} {pc0} {pc1} {len(seq)}')

        if both_finished or both_waiting:
            if both_waiting:
                print( f'Deadlock: {pc0} {pc1}')
            print( send_count0, send_count1)
            return send_count1

def sim3(seq):
    tbl0, pc0 = { 'p': 0}, 0
    tbl1, pc1 = { 'p': 1}, 0
    
    q0to1, q1to0 = deque(), deque()

    while True:
        waiting0, waiting1 = False, False
        while 0 <= pc0 < len(seq):
            tbl0, pc0, waiting0 = step( 0, seq, tbl0, pc0, q1to0, q0to1)
            if waiting0:
                break
        while 0 <= pc1 < len(seq):
            tbl1, pc1, waiting1 = step( 1, seq, tbl1, pc1, q0to1, q1to0)
            if waiting1:
                break

        print( f'{waiting0} {waiting1} {pc0} {pc1} {len(seq)}')

        if not( 0 <= pc0 < len(seq)) and not ( 0 <= pc1 < len(seq)) or \
           waiting0 and waiting1 and not q1to0 and not q0to1:
            print( send_count0, send_count1)
            return send_count1

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

    pc = 0
    sent_value = None
    count = 0

    while 0 <= pc < len(seq): # and count < 100:
        tup = seq[pc]
        #print(tbl,pc,sent_value,tup,end=' ')
        if tup[0] == 'set':
            set_value( tup[1], get_value(tup[2]))
        elif tup[0] == 'add':
            set_value( tup[1], get_value(tup[1]) + get_value(tup[2]))
        elif tup[0] == 'mul':
            set_value( tup[1], get_value(tup[1]) * get_value(tup[2]))
        elif tup[0] == 'mod':
            set_value( tup[1], get_value(tup[1]) % get_value(tup[2]))
        elif tup[0] == 'jgz':
            cond = get_value(tup[1])
            if cond > 0:
                pc += get_value(tup[2]) - 1
        elif tup[0] == 'snd':
            sent_value = get_value(tup[1])
        elif tup[0] == 'rcv':
            cond = get_value(tup[1])
            if cond != 0:
                return sent_value
        else:
            assert False, tup
        pc += 1
        #print(tbl,pc,sent_value)
        count += 1

    return None

def main(fp):
    seq = parse(fp)
    return sim(seq)

def main2(fp):
    seq = parse(fp)
    return sim3(seq)

@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 4 == main(fp)

@pytest.mark.skip
def test_AA():
    with open("data1","rt") as fp:
        assert 3 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))


