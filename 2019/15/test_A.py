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

import curses
import random

def main(fp,part2=False):
    insts = parse(fp)

    computer = gen_run(insts)

    screen = curses.initscr()
    #screen = None

    board = {}

    p = (0,0)
    movement_command = 1 # north
    # (x,y) x going right, y going down
    dirs = { 1: (0,-1), 2: (0,1), 3: (-1,0), 4: (1,0)}

    order = [1, 3, 2, 4]

    def test_move( movement_command):
        rc = next(computer)
        assert rc is None
        return computer.send(movement_command)

    def draw( p, v):
        if screen is not None:
            row, col = p[1] + 30, p[0] + 30
            if 0 <= row < 60 and 0 <= col < 100:
                screen.addch( row, col, v)

    def set_board( p, v):
        board[p] = v
        draw( p, v)

    def opposite( k):
        return order[ (order.index(k)+2)%4]

    sp = { p : []}
    reached = set()
    frontier = { p }

    levels = 0

    oxygen_at_level = None
    oxygen_p = None

    while frontier:

        new_frontier = set()
        for p in frontier:

            # travel from origin to p
            #print( f'path to {p}: {sp[p]}')
            q = (0,0)
            for k in sp[p]:
                status = test_move( k)                
                assert status in [1,2], (k, status)
                d = dirs[k]
                q = q[0]+d[0], q[1]+d[1]
            assert p == q

            # find walls around p
            for k,d in dirs.items():
                q = p[0]+d[0], p[1]+d[1]
                if q not in board: # unknown
                    status = test_move( k)
                    if status == 1:
                        set_board( q, '.')
                        test_move( opposite(k))
                    elif status == 2:
                        set_board( q, 'O')
                        if oxygen_at_level is None:
                            oxygen_at_level = levels+1
                            oxygen_p = q
                        test_move( opposite(k))
                    elif status == 0:
                        set_board( q, '#')
                    else:
                        assert False, status

            for k,d in dirs.items():
                q = p[0]+d[0], p[1]+d[1]
                assert q in board
                if board[q] != '#':
                    new_frontier.add( q)
                    if q not in frontier and q not in reached and q not in sp:
                        sp[q] = sp[p] + [k]

            # travel back to origin
            q = p
            for k in reversed(sp[p]):
                status = test_move( opposite(k))                
                assert status in [1,2], (k, opposite(k), status)
                d = dirs[opposite(k)]
                q = q[0]+d[0], q[1]+d[1]
            assert q == (0,0)
        
        levels += 1
        reached = reached.union(frontier)

        frontier = new_frontier.difference(reached)

        if screen is not None:
            screen.refresh()
            curses.napms(0)

    if screen is not None:
        curses.napms(10000)
        curses.endwin()

    if not part2:
        return oxygen_at_level

    reached = set()
    frontier = { oxygen_p }

    levels = 0

    while frontier:

        new_frontier = set()
        for p in frontier:
            for k,d in dirs.items():
                q = p[0]+d[0], p[1]+d[1]
                assert q in board
                if board[q] != '#':
                    new_frontier.add( q)

        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)
        if not frontier:
            break

        levels += 1

    print(levels)

    return levels

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main(fp,part2=True))



