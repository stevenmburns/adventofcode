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
        elif op == 5:
            if get_operand( modebits[1], seq_tbl[pc+1]) != 0:
                pc = get_operand( modebits[2], seq_tbl[pc+2])
            else:
                pc += 3
        elif op == 6:
            if get_operand( modebits[1], seq_tbl[pc+1]) == 0:
                pc = get_operand( modebits[2], seq_tbl[pc+2])
            else:
                pc += 3
        elif op in insts:
            a = get_operand( modebits[1], seq_tbl[pc+1])
            b = get_operand( modebits[2], seq_tbl[pc+2])
            set_value_to_operand( modebits[3], seq_tbl[pc+3], insts[op]( a, b))
            pc += 4            
        else:
            assert False, modebits

import time
def print_board( board):
    print('\033c',end='')

    mx, Mx = 0, 10
    my, My = 0, 10

    led = None
    for (x,y) in board.keys():
        if (x,y) == (-1,0):
            led = board[(x,y)]
            continue
        if my is None or my > y: my = y 
        if My is None or My < y: My = y 
        if mx is None or mx > x: mx = x 
        if Mx is None or Mx < x: Mx = x 

    print(f'led {led}')
    for y in range( my,My+1):
        line = ''
        for x in range( mx,Mx+1):
            q = (x,y) 
            if q in board:
                if board[q] in [1,2,3,4]:
                    line += str(board[q])
                else:
                    line += '.'
            else:
                line += '.'
        print(line)

def main(fp,part2=False):
    insts = parse(fp)

    print(insts)

    computer = gen_run(insts)        

    board = {}

    while True:
        try:
            x = next(computer)    
            y = next(computer)    
            tile_id = next(computer)    
        except StopIteration:
            break

        board[ (x,y)] = tile_id

    print_board(board)

    return sum( 1 for k,v in board.items() if v == 2)

import curses

def main2(fp,part2=False):
    insts = parse(fp)

    insts[0] = 2 # add quarters

    computer = gen_run(insts)

    screen = curses.initscr()

    board = {}

    joystick = None

    paddle = None
    ball = None

    steps = 0
    while True:
        try:
            x = next(computer) # does is want an input?
            if x is None: # yes, so send it
                x = computer.send(joystick)
            y = next(computer)
            tile_id = next(computer)
            assert x is not None
            assert y is not None
            assert tile_id is not None
        except StopIteration:
            break

        board[ (x,y)] = tile_id

        if x >= 0 and y >= 0:
            if tile_id != 0:
                screen.addch( y, x, str(tile_id))
            else:
                screen.addch( y, x, ' ')
            screen.refresh()
            curses.napms(0)

        if tile_id == 4:
            ball = (x,y)

        if tile_id == 3:
            paddle = (x,y)

        if ball is not None and paddle is not None:
            # adjust joystick to move paddle to ball
            if ball[0] > paddle[0]:
                joystick = 1
            elif ball[0] < paddle[0]:
                joystick = -1
            else:
                joystick = 0

        if steps % 1 == 0:
            pass
            #time.sleep(0.01)
            #print_board(board)
        steps += 1

    #print_board(board)
    curses.napms(3000)
    curses.endwin()

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))

if __name__ == "__main__":
    test_BB()



