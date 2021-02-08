import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []
    test_seq = []

    p = re.compile(r'^(x|y)=(\d+), (x|y)=(\d+)\.\.(\d+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m

        t=m.groups()
        seq.append( (t[0], int(t[1]), t[2], (int(t[3]), int(t[4]))))

    return seq

def main(fp):
    seq = parse(fp)

    seq_save = seq[:]

    mX, MX = None, None
    mY, MY = None, None

    for common, v, opposite, (lb,ub) in seq:
        assert common in "xy" and opposite in "xy" and common != opposite

        if common == 'x':
            if mX is None or mX > v: mX = v
            if MX is None or MX < v: MX = v
        elif common == 'y':
            if mY is None or mY > v: mY = v
            if MY is None or MY < v: MY = v
        else:
            assert False, common

        if opposite == 'x':
            if mX is None or mX > lb: mX = lb
            if MX is None or MX < ub: MX = ub
        elif opposite == 'y':
            if mY is None or mY > lb: mY = lb
            if MY is None or MY < ub: MY = ub
        else:
            assert False, opposite

    print(mX,MX,mY,MY)

    save_mY = mY

    assert mX <= 500 <= MX

    mY = 0

    print( f'Raster size: {(MX-mX+1)*(MY-mY+1)}')

    board = defaultdict(lambda: '.')

    board[ (500,0)] = '+'

    for common, v, opposite, (lb,ub) in seq:    
        if   common == 'x':
            for y in range(lb,ub+1):
                board[(v,y)] = '#'
        elif common == 'y':
            for x in range(lb,ub+1):
                board[(x,v)] = '#'
        else:
            assert False, common


    save_board = dict(board.items())


    def down( p):
        horiz_candidates = set()

        x,y = p
        for yy in range(y,MY+1):
            cand = board[(x,yy)] 
            if cand in '+|':
                pass
            elif cand == '.':
                board[(x,yy)] = '|'
                horiz_candidates.add( (x,yy))
            elif cand == '~':
                break
            elif cand == '#':
                break
            else:
                assert False, cand

        return horiz_candidates

    def horiz( p):
        horiz_candidates = set()
        down_candidates = set()


        x,y = p

        if board[p] != '|':
            return horiz_candidates, down_candidates

        assert board[p] == '|' and board[(x,y+1)] in "#~"

        lx = x-1
        while board[(lx,y)] in '.|' and mX - 1 <= lx <= MX + 1:
            lx -= 1
        lx += 1

        ux = x+1
        while board[(ux,y)] in '.|' and mX - 1 <= ux <= MX + 1:
            ux += 1
        ux -= 1

        in_well = True
        for xx in range(lx,ux+1):
            if board[(xx,y+1)] not in "#~":
                in_well = False

        if in_well:
            for xx in range(lx,ux+1):
                board[(xx,y)] = '~'
                if board[(xx,y-1)] == '|':
                    horiz_candidates.add( (xx,y-1))

            return horiz_candidates, down_candidates

        lx = x-1
        while board[(lx,y+1)] in "#~" and board[(lx,y)] != '#' and board[(lx-1,y)] != '#' and mX - 1 <= lx <= MX + 1:
            logging.info( f'lx {lx} y {y}')
            lx -= 1

        ux = x+1
        while board[(ux,y+1)] in "#~" and board[(ux,y)] != '#' and board[(ux+1,y)] != '#' and mX - 1 <= ux <= MX + 1:
            logging.info( f'ux {ux} y {y}')
            ux += 1

        for xx in range(lx,ux+1):
            if  board[(xx,y)] == '.':
                board[(xx,y)] = '|'
                down_candidates.add( (xx,y))
                
        return horiz_candidates, down_candidates


    def filter_horiz(gen):
        for (x,y) in gen:
            if board[(x,y)] == '|' and board[(x,y+1)] in "#~":
                    yield (x,y)
    def filter_down(gen):
        for (x,y) in gen:
            if board[(x,y)] == '|' and board[(x,y+1)] in ".":
                yield (x,y)

    def print_board(ymin=None,ymax=None):
        for y in range(mY,MY+1):
            line = ''
            for x in range(mX-1,MX+2):
                line += board[ (x,y)]
            if ymin is not None and y<ymin: continue
            if ymax is not None and y>ymax: continue
            print(line)

    horiz_candidates = down( (500,0))
    down_candidates = set()
    
    iter = 0
    while True:
        print( 'Candidate sizes', len(horiz_candidates), len(down_candidates))
        lst0 = list(filter_horiz(horiz_candidates))
        horiz_candidates = set()
        for p in lst0:
            hc, dc = horiz(p)
            horiz_candidates = horiz_candidates.union(hc)
            down_candidates = down_candidates.union(dc)
            #print()
            #print_board()
        lst1 = list(filter_down(down_candidates))
        down_candidates = set()
        for p in lst1:
            hc = down(p)
            horiz_candidates = horiz_candidates.union(hc)
            #print()
            #print_board()
        if not lst0 and not lst1:
            break
        iter += 1
        if False and iter > 34:
            break

    def count_water():
        count = 0
        for y in range(save_mY,MY+1):
            for x in range(mX-1,MX+2):
                if board[(x,y)] in '|~+':
                    count += 1
        return count

    def count_still_water():
        count = 0
        for y in range(save_mY,MY+1):
            for x in range(mX-1,MX+2):
                if board[(x,y)] in '~':
                    count += 1
        return count

    print()
    print_board()

    for (x,y), c in save_board.items():
        if c in '+#':
            assert board[(x,y)] == c, (x,y)


    return count_water(), count_still_water()


#@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 57, 29 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))
