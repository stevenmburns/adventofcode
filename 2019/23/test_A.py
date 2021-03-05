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

class IntCode:
    def __init__(self, seq):
        self.pc = 0
        self.offset = 0

        self.input_queue = deque()
        self.output_queue = deque()

        self.seq_tbl = defaultdict(int)
        for idx,inst in enumerate(seq):
            self.seq_tbl[idx] = inst

    def step(self):

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
                return self.seq_tbl[val]
            elif mode == 1:
                return val
            elif mode == 2:
                return self.seq_tbl[val+self.offset]
            else:
                assert False, mode

        def set_value_to_operand( mode, val, value):
            if mode == 0:
                self.seq_tbl[val] = value
            elif mode == 1:
                assert False
            elif mode == 2:
                self.seq_tbl[val+self.offset] = value
            else:
                assert False, mode

        cmd = self.seq_tbl[self.pc]
        op = cmd % 100

        cmd = cmd // 100
        modebits = [op]
        for _ in range(3):
            modebits.append(cmd % 10)
            cmd = cmd // 10

        if self.seq_tbl[self.pc] == 99:
            return True

        if op == 3:
            # non-blocking version
            if self.input_queue:
                input_value = self.input_queue.pop()
            else:
                input_value = -1
            set_value_to_operand( modebits[1], self.seq_tbl[self.pc+1], input_value)
            self.pc += 2
        elif op == 4:
            self.output_queue.appendleft( get_operand( modebits[1], self.seq_tbl[self.pc+1]))
            self.pc += 2
        elif op == 9:
            self.offset += get_operand( modebits[1], self.seq_tbl[self.pc+1])
            self.pc += 2
        elif op in jumps:
            a = get_operand( modebits[1], self.seq_tbl[self.pc+1])
            b = get_operand( modebits[2], self.seq_tbl[self.pc+2])
            self.pc = b if jumps[op]( a) else self.pc+3
        elif op in insts:
            a = get_operand( modebits[1], self.seq_tbl[self.pc+1])
            b = get_operand( modebits[2], self.seq_tbl[self.pc+2])
            set_value_to_operand( modebits[3], self.seq_tbl[self.pc+3], insts[op]( a, b))
            self.pc += 4            
        else:
            assert False, modebits

        return False

def main(fp):
    insts = parse(fp)

    computers = [ IntCode(insts) for _ in range(50)]

    for idx,computer in enumerate(computers):
        computer.input_queue.appendleft( idx)
        computer.input_queue.appendleft( -1)

    sent_to_255 = None

    save_Y = None

    all_empty_for = 0

    queues = [ deque() for _ in range(50)]

    for _ in range(1000000):

        for idx,computer in enumerate(computers):    
            if computer.step():
                assert False, f'{idx} stop early'

        for idx,computer in enumerate(computers):

            count = 0
            while computer.output_queue:
                val = computer.output_queue.pop()
                print( f'output {idx} {val}')
                queues[idx].appendleft( val)
                count += 1
            assert count <= 1
        
            assert len(queues[idx]) <= 3
            if len(queues[idx]) == 3:
                addr = queues[idx].pop()
                x = queues[idx].pop()
                y = queues[idx].pop()
                assert len(queues[idx]) == 0

                if addr == 255:
                    print( f'Sent to 255 {(x,y)}')
                    sent_to_255 = (x,y)
                else:
                    print( f'Enqueuing {addr} {(x,y)}')
                    assert 0 <= addr < 50, addr
                    computers[addr].input_queue.appendleft( x)
                    computers[addr].input_queue.appendleft( y)
            
        all_empty2 = all( not queue for queue in queues)

        all_empty = all( not computer.input_queue for computer in computers)

        if all_empty and all_empty2:
            all_empty_for += 1
        else:
            all_empty_for = 0

        if all_empty_for >= 1000:
            print( f'SMB {all_empty_for} {sent_to_255} {save_Y}')
            all_empty_for = 0

            assert sent_to_255 is not None

            if sent_to_255[1] == save_Y:
                return save_Y

            print(f'Sent to 0 {sent_to_255}')
            computers[0].input_queue.appendleft( sent_to_255[0])
            computers[0].input_queue.appendleft( sent_to_255[1])

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
