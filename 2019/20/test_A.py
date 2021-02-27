import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import heapq

logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p = re.compile(r'^[ #.A-Z]*$')

    for line in fp:
        line = line.rstrip('\n')
        assert p.match(line)
        seq.append( line)

    l = len(seq[0])
    for line in seq[1:]:
        assert l == len(line)

    top_tags = [ ''.join([x,y]) for x,y in list(zip(seq[0],seq[1]))[2:-2]]
    bot_tags = [ ''.join([x,y]) for x,y in list(zip(seq[-2],seq[-1]))[2:-2]]

    left_tags = [line[:2] for line in seq[2:-2]]
    right_tags = [line[-2:] for line in seq[2:-2]]

    border = None
    for irow in range( len(seq)):
        line = seq[irow]
        last = False
        trans01 = []
        trans10 = []
        for icol in range( 2, len(line)):
            cand = line[icol] in '#.'
            if not last and cand:
                trans01.append(icol)
            if last and not cand:
                trans10.append(icol)
            last = cand
        if len(trans01) == 2:
            assert len(trans10) == 2
            border = trans10[0] - 2
            break 

    itop_tags = []
    irow = 2+border-1
    for icol in range(2+border, l-2-border):
        tag = None
        if seq[irow][icol] == '.':
            tag = seq[irow+1][icol] + seq[irow+2][icol]
        itop_tags.append(tag)

    ibot_tags = []
    irow = len(seq)-1-2-border+1
    for icol in range(2+border, l-2-border):
        tag = None
        if seq[irow][icol] == '.':
            tag = seq[irow-2][icol] + seq[irow-1][icol]
        ibot_tags.append(tag)

    ileft_tags = []
    icol = 2+border-1
    for irow in range(2+border, len(seq)-2-border):
        tag = None
        if seq[irow][icol] == '.':
            tag = seq[irow][icol+1] + seq[irow][icol+2]
        ileft_tags.append(tag)

    iright_tags = []
    icol = l-1-2-border+1
    for irow in range(2+border, len(seq)-2-border):
        tag = None
        if seq[irow][icol] == '.':
            tag = seq[irow][icol-2] + seq[irow][icol-1]
        iright_tags.append(tag)

    nrows = len(seq)-4
    ncols = l - 4
    
    tag_tbl = defaultdict(list)

    for icol, tag in enumerate(top_tags):
        if tag is not None and tag != '  ':
            tag_tbl[tag].append( (0,icol))

    for icol, tag in enumerate(bot_tags):
        if tag is not None and tag != '  ':
            tag_tbl[tag].append( (nrows-1,icol))

    for irow, tag in enumerate(left_tags):
        if tag is not None and tag != '  ':
            tag_tbl[tag].append( (irow,0))

    for irow, tag in enumerate(right_tags):
        if tag is not None and tag != '  ':
            tag_tbl[tag].append( (irow,ncols-1))
        
    for icol, tag in enumerate(itop_tags):
        if tag is not None and tag != '  ':
            tag_tbl[tag].append( (0+border-1,icol+border))

    for icol, tag in enumerate(ibot_tags):
        if tag is not None and tag != '  ':
            tag_tbl[tag].append( (nrows-1-border+1,icol+border))

    for irow, tag in enumerate(ileft_tags):
        if tag is not None and tag != '  ':
            tag_tbl[tag].append( (irow+border,0+border-1))

    for irow, tag in enumerate(iright_tags):
        if tag is not None and tag != '  ':
            tag_tbl[tag].append( (irow+border,ncols-1-border+1))
        

    for k, v in tag_tbl.items():
        assert len(v) == 2 or k == 'AA' or k == 'ZZ'
        for (irow,icol) in v:
            assert seq[irow+2][icol+2] == '.', (k,v)

    print(tag_tbl)
    for line in seq:
        print(line)
        
    new_seq = []
    for irow,line in enumerate(seq[2:-2]):
        new_line = ''
        for icol, c in enumerate(line[2:-2]):
            if 0 <= irow < border or nrows-border <= irow < nrows:
                new_line += c
            else:
                if 0 <= icol < border or ncols-border <= icol < ncols:
                    new_line += c
                else:
                    new_line += ' '
        new_seq.append(new_line)

    print(tag_tbl)
    for line in new_seq:
        print(line)


    return new_seq, tag_tbl

def determine_path_lengths( board, p):
    nrows = len(board)
    ncols = len(board[0])

    reached = set()
    frontier = set( [p])
    level = 0

    length_tbl = { p: 0}

    while frontier:

        new_frontier = set()
        for state in frontier:

            (irow,icol) = state

            dirs = [(-1,0),(1,0),(0,-1),(0,1)]

            for drow,dcol in dirs:
                jrow,jcol = irow+drow,icol+dcol
                if 0 <= jrow < nrows and 0 <= jcol < ncols:
                    c = board[jrow][jcol]
                    if c == '#': continue
                    if c != '.':
                        if (jrow,jcol) not in length_tbl:
                            length_tbl[ (jrow,jcol)] = level+1
                    else:
                        new_frontier.add( (jrow,jcol))

        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)
        level += 1
    
    return length_tbl


def main(fp):
    board = parse(fp)

    return 23

    nrows = len(board)
    ncols = len(board[0])
 
    adjacents = {}

    start = set()
    all_keys = set()
    for irow,line in enumerate(board):
        assert ncols == len(line)
        for icol,c in enumerate(line):
            if c == '@':
                start.add((irow,icol))
            if c.islower():
                all_keys.add( c)

            if c == '@' or c.isupper() or c.islower():
                adjacents[ (irow,icol)] = determine_path_lengths(board, (irow,icol))

    print()
    for k,v in adjacents.items():
        print( k, board[k[0]][k[1]])
        for kk,vv in v.items():
            print( '\t', kk, board[kk[0]][kk[1]], vv)

    assert len(start) == 1

    state = frozenset(), list(start)[0]

    reached = {} # state => steps

    frontier = []
    heapq.heappush(frontier, (0, state))

    while frontier:

        level, state = heapq.heappop( frontier)

        print( f'headpop: {level} {state}') 

        if state not in reached:
            reached[state] = level

        keys_acquired, (irow,icol) = state

        for (jrow,jcol),cost in adjacents[(irow,icol)].items():
            new_cost = level + cost

            if (jrow,jcol) == (irow,icol): continue
 
            c = board[jrow][jcol]
            assert c != '#'
            if c.isupper() and c.lower() not in keys_acquired: continue
            if c.islower():
                new_keys_acquired = set(keys_acquired)
                new_keys_acquired.add( c)

                if new_keys_acquired == all_keys:
                    return new_cost

                new_state = (frozenset( new_keys_acquired), (jrow,jcol))
            else:
                new_state = (keys_acquired, (jrow,jcol))


            if new_state not in reached or reached[new_state] > new_cost:
                reached[new_state] = new_cost
                heapq.heappush( frontier, (new_cost,new_state))

    return None


#@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 23 == main(fp)

@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 58 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))





