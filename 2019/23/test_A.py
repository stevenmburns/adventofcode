import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( [ int(x) for x in line.split(',')])

    assert len(seq) == 1

    return seq[0]

def gen_run(seq):
    pc = 0
    offset = 0

    seq_tbl = defaultdict(int)
    for idx,inst in enumerate(seq):
        seq_tbl[idx] = inst

    insts = { 1: lambda x,y: x+y,
              2: lambda x,y: x*y,
              7: lambda x,y: 1 if x < y else 0,
              8: lambda x,y: 1 if x == y else 0
    }

    jumps = { 5: lambda x: x != 0,
              6: lambda x: x == 0
    }

    def get_operand( mode, val):
        if mode == 0:
            return seq_tbl[val]
        elif mode == 1:
            return val
        elif mode == 2:
            return seq_tbl[val+offset]
        else:
            assert False, mode

    def set_value_to_operand( mode, val, value):
        if mode == 0:
            seq_tbl[val] = value
        elif mode == 1:
            assert False
        elif mode == 2:
            seq_tbl[val+offset] = value
        else:
            assert False, mode

    while True:
        cmd = seq_tbl[pc]
        op = cmd % 100


        cmd = cmd // 100
        modebits = [op]
        for _ in range(3):
            modebits.append(cmd % 10)
            cmd = cmd // 10

        if seq_tbl[pc] == 99:
            break

        if op == 3:
            set_value_to_operand( modebits[1], seq_tbl[pc+1], (yield))
            pc += 2
        elif op == 4:
            yield get_operand( modebits[1], seq_tbl[pc+1])
            pc += 2
        elif op == 9:
            offset += get_operand( modebits[1], seq_tbl[pc+1])
            pc += 2
        elif op in jumps:
            a = get_operand( modebits[1], seq_tbl[pc+1])
            b = get_operand( modebits[2], seq_tbl[pc+2])
            pc = b if jumps[op]( a) else pc+3
        elif op in insts:
            a = get_operand( modebits[1], seq_tbl[pc+1])
            b = get_operand( modebits[2], seq_tbl[pc+2])
            set_value_to_operand( modebits[3], seq_tbl[pc+3], insts[op]( a, b))
            pc += 4            
        else:
            assert False, modebits

import curses
import random

def main(fp):
    insts = parse(fp)

    computers = [ gen_run(insts[:]) for _ in range(50)]

    for idx,computer in enumerate(computers):
        assert next(computer) is None
        assert computer.send(idx) is None


    queues = [ deque() for _ in range(50)]

    sent_to_255 = None

    save_Y = None

    all_empty_for = 0

    for _ in range(1000000):
        for idx,computer in enumerate(computers):    

            returned = deque()

            if not queues[idx]:
                rc = computer.send(-1) 
                if rc is not None:
                    returned.appendleft( rc)
            else:
                (x,y) = queues[idx].pop()
                rc = computer.send(x)
                if rc is not None:
                    returned.appendleft( rc)
                rc = computer.send(y)
                if rc is not None:
                    returned.appendleft( rc)

            if len(returned) == 1:
                addr = returned[0]
                x = next(computer)
                y = next(computer)

            if len(returned) == 2:
                print(f'unusual {returned}')
                addr, x = returned[1], returned[0]
                y = next(computer)

            if len(returned) > 0:
                if addr == 255:
                    print( f'Sent to 255 {(x,y)}')
                    sent_to_255 = (x,y)
                else:
                    assert 0 <= addr < 50, addr
                    queues[addr].appendleft( (x,y))

        all_empty = all( not queue for queue in queues)

        if all_empty:
            all_empty_for += 1
        else:
            all_empty_for = 0

        if all_empty_for > 100:
            print( f'SMB {all_empty_for} {sent_to_255} {save_Y}')
            all_empty_for = 0
            if sent_to_255[1] == save_Y:
                return save_Y


            print(f'Sent to 0 {sent_to_255}')
            queues[0].appendleft( sent_to_255)

            save_Y = sent_to_255[1]

        last_all_empty = all_empty

    return None


#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))
