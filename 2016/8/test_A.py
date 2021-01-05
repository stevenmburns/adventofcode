import pytest
import io
import re
import hashlib

class RectCommand:
    def __init__(self, ncols, nrows):
        self.nrows = nrows
        self.ncols = ncols
    def __repr__(self):
        return f"RectCommand( {self.ncols}, {self.nrows})"
    def modify(self, display):
        for irow in range(self.nrows):
            for icol in range(self.ncols):
                display[irow][icol] = True

class RotateRowCommand:
    def __init__(self, irow, amount):
        self.irow = irow
        self.amount = amount
    def __repr__(self):
        return f"RotateRowCommand( {self.irow}, {self.amount})"
    def modify(self, display):
        row = display[self.irow]
        new_row = [ row[(icol-self.amount)%len(display[0])] for icol in range(len(display[0]))]
        display[self.irow] = new_row


class RotateColumnCommand:
    def __init__(self, icol, amount):
        self.icol = icol
        self.amount = amount
    def __repr__(self):
        return f"RotateColumnCommand( {self.icol}, {self.amount})"
    def modify(self, display):
        col = [ display[irow][self.icol] for irow in range(len(display))]
        new_col = [ col[(irow-self.amount)%len(display)] for irow in range(len(display))]
        for irow in range(len(display)):
            display[irow][self.icol] = new_col[irow]

def parse(fp):
    seq = []
    p_rect = re.compile(r'^rect (\d+)x(\d+)$')
    p_row = re.compile(r'^rotate row y=(\d+) by (\d+)$')
    p_col = re.compile(r'^rotate column x=(\d+) by (\d+)$')

    for line in fp:
        line = line.rstrip('\n')

        m = p_rect.match(line)
        if m:
            seq.append( RectCommand( int(m.groups()[0]),int(m.groups()[1])))
            continue

        m = p_row.match(line)
        if m:
            seq.append( RotateRowCommand( int(m.groups()[0]),int(m.groups()[1])))
            continue
        
        m = p_col.match(line)
        if m:
            seq.append( RotateColumnCommand( int(m.groups()[0]),int(m.groups()[1])))
            continue




        assert False, line

    return seq

def step( display): 
    pass

def print_display( display):
    for row in display:
        print( ''.join( '#' if x else '.' for x in row))

def count_display( display):
    count = 0
    for row in display:
        count += sum(1 for x in row if x)
    return count
    
def main(fp,screen_size):
    seq = parse(fp)
    print(seq)

    display = [ [False]*screen_size[1] for _ in range(screen_size[0])]



    print_display(display)
    for cmd in seq:
        cmd.modify(display)
        print("==========")
        print_display(display)

    return count_display(display)

def test_A():
    with open('data0', 'rt') as fp:
        assert 6 == main(fp,(3,7))

def test_B():
    with open('data', 'rt') as fp:
        print(main(fp,(6,50)))
