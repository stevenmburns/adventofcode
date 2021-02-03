import pytest
import io
import re
import itertools
from collections import defaultdict

dir2c = { (1,0): 'v', (-1,0): '^', (0,1): '>', (0,-1): '<'}
c2dir = { v: k for k,v in dir2c.items()}
next_state = { 'L': 'S', 'S': 'R', 'R': 'L'}
left_turn = { a:b for a,b in zip("<>^v", "v^<>")}
right_turn = { a:b for a,b in zip("<>^v", "^v><")}
forward_slash = { a:b for a,b in zip("<>^v", "v^><")}
backward_slash = { a:b for a,b in zip("<>^v", "^v<>")}

class Cart:
    def __init__( self, irow, icol, c):
        self.irow = irow
        self.icol = icol
        self.drow = None
        self.dcol = None
        self.set_dir(c)
        self.state = 'L'

    def toPos(self):
        return self.irow,self.icol

    def __repr__(self):
        return str( (self.irow,self.icol,self.drow,self.dcol,self.state))

    def set_dir(self, c):
        self.drow, self.dcol = c2dir[c]

    def incr_state(self):
        self.state = next_state[self.state]

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)
    return seq

def extract_carts(board):
    carts = []
    newboard = []
    for i,line in enumerate(board):
        newline = ''
        for j,c in enumerate(line):
            if c in "<>^v":
                carts.append( Cart(i,j,c))
                if c in "<>":
                    newline += "-"
                else:
                    newline += "|"
            else:
                newline += c
        newboard.append(newline)
            
    return carts, newboard

def print_board( carts, board):
    positions = defaultdict(list)
    for idx,cart in enumerate(carts):
        positions[cart.toPos()].append(idx)

    for i,line in enumerate(board):
        newline = ''
        for j,c in enumerate(line):
            if (i,j) in positions:
                if len(positions[(i,j)]) > 1:
                    newc = 'X'
                else:
                    cart = carts[positions[(i,j)][0]]
                    newc = dir2c[(cart.drow,cart.dcol)]
            else:
                newc = c
            newline += newc
        print(newline)

def step( carts, board):
    first_crash_location = None
    positions = { cart.toPos() for cart in carts}
    for cart in carts:
        # Should always be able to go forward one
        jrow,jcol = cart.irow+cart.drow,cart.icol+cart.dcol
        c = board[jrow][jcol] 
        assert c != ' '
        d = cart.drow,cart.dcol
        if c == '+':
            """change dir based on state"""
            if cart.state == 'L':
                cart.drow,cart.dcol = c2dir[left_turn[dir2c[d]]]
            elif cart.state == 'R':
                cart.drow,cart.dcol = c2dir[right_turn[dir2c[d]]]
            elif cart.state == 'S':
                pass
            else:
                assert False, (cart.drow,cart.dcol,cart.state)
            cart.incr_state()
        elif c == '/':
            cart.drow,cart.dcol = c2dir[forward_slash[dir2c[d]]]
        elif c == '\\':
            cart.drow,cart.dcol = c2dir[backward_slash[dir2c[d]]]
        else:
            pass

        positions.remove(cart.toPos())

        cart.irow,cart.icol = jrow,jcol
        if first_crash_location is None and cart.toPos() in positions:
            first_crash_location = cart.toPos()
            
        positions.add(cart.toPos())

    carts.sort(key=lambda o: o.toPos())
    return first_crash_location



def main(fp):
    board = parse(fp)

    print('Raw board')
    for line in board:
        print(line)

    carts, board = extract_carts(board)

    print(carts)
    print_board(carts, board)
    for _ in range(10000):
        first_crash_location = step(carts, board)
        #print(carts)
        #print_board(carts, board)
        if first_crash_location is not None:
            break

    return first_crash_location[1],first_crash_location[0]

def step2( carts, board):
    positions = { cart.toPos():idx for idx,cart in enumerate(carts)}

    crashed_carts = set()

    for cart_idx,cart in enumerate(carts):
        print( cart_idx, cart, positions, crashed_carts)
        if cart_idx in crashed_carts: continue
        
        # Should always be able to go forward one
        jrow,jcol = cart.irow+cart.drow,cart.icol+cart.dcol
        c = board[jrow][jcol] 
        assert c != ' '
        d = cart.drow,cart.dcol
        if c == '+':
            """change dir based on state"""
            if cart.state == 'L':
                cart.drow,cart.dcol = c2dir[left_turn[dir2c[d]]]
            elif cart.state == 'R':
                cart.drow,cart.dcol = c2dir[right_turn[dir2c[d]]]
            elif cart.state == 'S':
                pass
            else:
                assert False, (cart.drow,cart.dcol,cart.state)
            cart.incr_state()
        elif c == '/':
            cart.drow,cart.dcol = c2dir[forward_slash[dir2c[d]]]
        elif c == '\\':
            cart.drow,cart.dcol = c2dir[backward_slash[dir2c[d]]]
        else:
            pass

        del positions[cart.toPos()]

        cart.irow,cart.icol = jrow,jcol
        if cart.toPos() in positions:
            crashed_carts.add(cart_idx)
            crashed_carts.add(positions[cart.toPos()])
            
        positions[cart.toPos()] = cart_idx

    carts = [ cart for idx,cart in enumerate(carts) if idx not in crashed_carts]

    carts.sort(key=lambda o: o.toPos())
    return carts

def main2(fp):
    board = parse(fp)


    carts, board = extract_carts(board)

    assert len(carts) % 2 == 1

    print(carts)
    print_board(carts, board)
    for _ in range(1000000):
        carts = step2(carts, board)
        #print(carts)
        #print_board(carts, board)
        if len(carts) == 1:
            p = carts[0].toPos()
            return p[1],p[0]

    return None

@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert (7,3) == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

def test_AA():
    with open("data1","rt") as fp:
        assert (6,4) == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))
