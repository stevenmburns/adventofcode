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

    computer = gen_run(insts)

    board = ''.join( chr(x) for x in computer).split('\n')[:-2]

    nrows = len(board)
    ncols = len(board[0])
    for irow in range(0,nrows):
        assert len(board[irow]) == ncols

    joints = set()
    dirs = [ (0,0), (-1,0), (1,0), (0,-1), (0,1)]
    for irow in range(1,nrows-1):
        for icol in range(1,ncols-1):
            if all( board[irow+drow][icol+dcol] == '#' for drow,dcol in dirs):
                joints.add( (irow,icol))

    return sum( irow*icol for irow,icol in joints)


def main2(fp):
    insts = parse(fp)
    insts[0] = 2 # run in game mode

    computer = gen_run(insts)

    dirs = { '<': (0,-1), '>': (0,1), '^': (-1,0), 'v': (1,0)}

    def recv_board():
        s = ''
        last_c = None
        while True:
            try:
                rc = next(computer)
                if rc is None:
                    break
                c = chr(rc)
                s += c
                if last_c is not None and last_c == '\n' and c == '\n':
                    return s
                last_c = c
            except StopIteration:
                break

        assert False, "Expected consecutive new lines to end board"

    def recv():
        s = ''
        while True:
            try:
                rc = next(computer)
                if rc is None:
                    break
                s += chr(rc)
            except StopIteration:
                break
        return s

    def recv_score():
        try:
            rc = next(computer)
            return rc
        except StopIteration:
            return None
        return s

    def legal_dirs( board, p):
        nrows = len(board)
        ncols = len(board[0])
        irow, icol = p
        assert board[irow][icol] != '.'


        result = set()
        for dir, (drow,dcol) in dirs.items():
            jrow,jcol = irow+drow,icol+dcol
            if  0 <= jrow < nrows and 0 <= jcol < ncols:
                if board[jrow][jcol] != '.':
                    result.add( (dir,(jrow,jcol)))
        
        return result

                    
    def analyze_board(s):
        board = s.split('\n')[:-2]
        order = '<^>v'

        nrows = len(board)
        ncols = len(board[0])

        def turn( before, now):
            bi = order.index(before)
            ni = order.index(now)

            delta = (ni-bi)%4

            assert delta in [1,3]
            if delta == 1:
                return 'R'
            elif delta == 3:
                return 'L'


        cursors = set()
        for irow,line in enumerate(board):
            for icol,c in enumerate(line):
                if c in order:
                    cursors.add( (irow,icol))

        assert len(cursors) == 1
        cursor = list(cursors)[0]
        
        d = board[cursor[0]][cursor[1]]

        print(cursor, d)

        def opposite( c):

            idx = order.index(c)
            return order[(idx+2)%4]

        moves = []

        last_d = d
        while True:
            s = legal_dirs( board, cursor)

            s = { x for x in s if x[0] != opposite(last_d)}

            if len(s) == 0:
                break

            assert len(s) == 1
            d, next_cursor = list(s)[0]
            drow,dcol = dirs[d]
            steps = 0
            while True:
                irow,icol = cursor
                jrow,jcol = irow+drow, icol+dcol
                if 0 <= jrow < nrows and 0 <= jcol < ncols and \
                   board[jrow][jcol] == '#':
                    cursor = jrow,jcol
                    steps += 1
                else:
                    break

            moves.append( (turn(last_d,d),steps))

            last_d = d

        return moves

    def send( s):
        result = []
        for c in s:
            rc = computer.send(ord(c))
            assert rc is None
        rc = computer.send(ord('\n'))
        return chr(rc)

    board = recv_board()

    print()
    print(board)

    flat_commands = analyze_board(board)

    print(flat_commands)

    for k in range(1,5):
        for i in range(len(flat_commands)-k+1):
            lst = flat_commands[i:i+k]
            print( lst, i, i+k)
            for j in range(len(flat_commands)-k+1):        
                if lst == flat_commands[j:j+k]:
                    print('\tmatch', j)

    for i in range(len(flat_commands)-4+1):
        lst = flat_commands[i:i+4]
        print( lst, i, i+4)
        for j in range(len(flat_commands)-4+1):        
            if lst == flat_commands[j:j+4]:
                print('\tmatch', j)

    """
[('L', 12), ('L', 8), ('R', 12)] 0 3
	match 0
	match 7
	match 13
	match 16


[('L', 10), ('L', 8), ('L', 12), ('R', 12)] 3 7
	match 3
	match 22
	match 29

[('R', 12), ('L', 8), ('L', 10)] 10 13
	match 10
	match 19
	match 26


"""


    sA = ','.join( f'{c},{n}' for c,n in flat_commands[0:3])
    sB = ','.join( f'{c},{n}' for c,n in flat_commands[3:7])
    sC = ','.join( f'{c},{n}' for c,n in flat_commands[10:13])


    print(recv())
    print( send( 'A,B,A,C,A,A,C,B,C,B'), end='')
    print(recv())
    print( send( sA), end='')
    print(recv())
    print( send( sB), end='')
    print(recv())
    print( send( sC), end='')
    print(recv())
    print( send( 'n'), end='')
    print(recv_board())

    score = next(computer)
    print(score)

    try:
        rc = next(computer)
        print( 'expected a Stopiteration')
    except StopIteration:
        pass


@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        assert 10632 == main(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))



