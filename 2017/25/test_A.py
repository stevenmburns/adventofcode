import sys
import pytest
import io
import re
import itertools
from collections import deque


def parse(fp):
    seq = []
    p_init = re.compile(r'^Begin in state (\S+)\.$') 
    p_steps = re.compile(r'^Perform a diagnostic checksum after (\d+) steps\.$')
 
    p_blank = re.compile(r'^$')
    p_instate = re.compile(r'^In state (\S+):$')

    p_current = re.compile(r'^  If the current value is (\d+):$')
    p_write = re.compile(r'^    - Write the value (\d+)\.$')
    p_move  = re.compile(r'^    - Move one slot to the (left|right)\.$')
    p_next  = re.compile(r'^    - Continue with state (\S+)\.$')

    initial_state = None
    diagnostic_stepnum = None

    current_state = None
    current_value = None

    tbl = {}

    for line in fp:
        line = line.rstrip('\n')
        m = p_init.match(line)
        if m:
            initial_state = m.groups()[0]
            continue
        m = p_steps.match(line)
        if m:
            diagnostic_stepnum = int(m.groups()[0])
            continue
        m = p_blank.match(line)
        if m:
            current_state = None
            current_value = None
            continue
        m = p_instate.match(line)
        if m:
            current_state = m.groups()[0]
            assert current_state not in tbl
            tbl[current_state] = {}
            continue
        m = p_current.match(line)
        if m:
            assert current_state is not None
            current_value = int(m.groups()[0])
            tbl[current_state][current_value] = [None,None,None]
            continue
        m = p_write.match(line)
        if m:
            assert current_state is not None
            assert current_value is not None
            tbl[current_state][current_value][0] = int(m.groups()[0])
            continue
        m = p_move.match(line)
        if m:
            assert current_state is not None
            assert current_value is not None
            tbl[current_state][current_value][1] = m.groups()[0]
            continue
        m = p_next.match(line)
        if m:
            assert current_state is not None
            assert current_value is not None
            tbl[current_state][current_value][2] = m.groups()[0]
            continue
        assert False, line

    assert initial_state is not None
    assert diagnostic_stepnum is not None

    return initial_state, diagnostic_stepnum, tbl

def sim(initial_state, n, tbl):
    tape = {}
    cursor = 0
    state = initial_state

    def g():
        return tape.get(cursor,0)

    def count_tape():
        count = 0
        for k,v in tape.items():
            if v == 1:
                count += 1
        return count

    for i in range(n):
        if i % 100000 == 0:
            print(i,cursor,state,count_tape())
        value, mv, next_state = tbl[state][g()]
        tape[cursor] = value
        if mv == 'left':
            cursor -= 1
        elif mv == 'right':
            cursor += 1
        else:
            assert False, mv
        state = next_state

    return count_tape()

def main(fp):
    initial_state, n, tbl = parse(fp)
    return sim(initial_state, n, tbl)

#@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 3 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))



