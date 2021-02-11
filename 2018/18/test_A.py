import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)

    l = len(seq[0])
    for line in seq[1:]:
        assert l == len(line)

    return seq



def aux(seq, iters):
    nrows = len(seq)
    ncols = len(seq[0])

    def gen_adjacent( p):
        irow, icol = p
        for drow in [-1,0,1]:
            for dcol in [-1,0,1]:
                if drow == 0 and dcol == 0: continue
                jrow, jcol = irow+drow, icol+dcol
                if 0 <= jrow < nrows and 0 <= jcol < ncols:
                    yield jrow, jcol

    def step_cell( p):
        irow, icol = p

        histo = defaultdict(int)
        for (jrow,jcol) in gen_adjacent(p):
            histo[seq[jrow][jcol]] += 1
        
        if seq[irow][icol] == '.':
            return '|' if histo['|'] >= 3 else '.'

        elif seq[irow][icol] == '|':        
            return '#' if histo['#'] >= 3 else '|'

        elif seq[irow][icol] == '#':        
            return '#' if histo['#'] >= 1 and histo['|'] else '.'

        else:
            assert False, (seq[irow][icol], irow, icol)

    
    def print_board():
        print()
        for line in seq:
            print(line)

    def counts():
        histo = defaultdict(int)
        for line in seq:
            for c in line:
                histo[c] += 1
        return histo

    #print_board()
    for _ in range(iters):
        new_seq = []
        for irow in range(nrows):
            line = ''
            for icol in range(ncols):
                line += step_cell( (irow,icol))
            new_seq.append(line)
        seq = new_seq
        #print_board()
        

    h = counts()

    return h['#'] * h['|']

def main(fp):
    seq = parse(fp)
    return aux(seq)


def main2(fp):
    seq = parse(fp)

    save_seq = seq[:]


    nrows = len(seq)
    ncols = len(seq[0])

    def gen_adjacent( p):
        irow, icol = p
        for drow in [-1,0,1]:
            for dcol in [-1,0,1]:
                if drow == 0 and dcol == 0: continue
                jrow, jcol = irow+drow, icol+dcol
                if 0 <= jrow < nrows and 0 <= jcol < ncols:
                    yield jrow, jcol

    def step_cell( p):
        irow, icol = p

        histo = defaultdict(int)
        for (jrow,jcol) in gen_adjacent(p):
            histo[seq[jrow][jcol]] += 1
        
        if seq[irow][icol] == '.':
            return '|' if histo['|'] >= 3 else '.'

        elif seq[irow][icol] == '|':        
            return '#' if histo['#'] >= 3 else '|'

        elif seq[irow][icol] == '#':        
            return '#' if histo['#'] >= 1 and histo['|'] else '.'

        else:
            assert False, (seq[irow][icol], irow, icol)

    
    def print_board():
        print()
        for line in seq:
            print(line)

    def counts():
        histo = defaultdict(int)
        for line in seq:
            for c in line:
                histo[c] += 1
        return histo

    states = { tuple(seq) : 0}

    result = None

    for i in range(1,100000):
        if i % 1000 == 0:
            print( i)
        new_seq = []
        for irow in range(nrows):
            line = ''
            for icol in range(ncols):
                line += step_cell( (irow,icol))
            new_seq.append(line)
        seq = new_seq
        state = tuple(seq)
        if state in states:
            result = states[state], i
            break
        states[state] = i

    print(result)

    iters = 1000000000

    i = (iters - result[0]) % (result[1]-result[0]) + result[0]

    for k,v in states.items():
        if v == i:
            seq = list(k)

    h = counts()

    result =  h['#'] * h['|']

    return result

@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 1147 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

@pytest.mark.skip
def test_AA():
    with open("data0","rt") as fp:
        print(main2(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))
