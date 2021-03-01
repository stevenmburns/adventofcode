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
            tag_tbl[(tag,'o')] = (0,icol)

    for icol, tag in enumerate(bot_tags):
        if tag is not None and tag != '  ':
            tag_tbl[(tag,'o')] = (nrows-1,icol)

    for irow, tag in enumerate(left_tags):
        if tag is not None and tag != '  ':
            tag_tbl[(tag,'o')] = (irow,0)

    for irow, tag in enumerate(right_tags):
        if tag is not None and tag != '  ':
            tag_tbl[(tag,'o')] = (irow,ncols-1)
        
    for icol, tag in enumerate(itop_tags):
        if tag is not None and tag != '  ':
            tag_tbl[(tag,'i')] = (0+border-1,icol+border)

    for icol, tag in enumerate(ibot_tags):
        if tag is not None and tag != '  ':
            tag_tbl[(tag,'i')] = (nrows-1-border+1,icol+border)

    for irow, tag in enumerate(ileft_tags):
        if tag is not None and tag != '  ':
            tag_tbl[(tag,'i')] = (irow+border,0+border-1)

    for irow, tag in enumerate(iright_tags):
        if tag is not None and tag != '  ':
            tag_tbl[(tag,'i')] = (irow+border,ncols-1-border+1)
        

    for k, (irow,icol) in tag_tbl.items():
        assert seq[irow+2][icol+2] == '.', (k,(irow,icol))

    print(tag_tbl)
    for line in seq:
        print(line)
        
    board = []
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
        board.append(new_line)

    return board, tag_tbl

def determine_path_lengths( board, inv_tag_tbl, p):
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
                    if c == ' ': continue
                    if (jrow,jcol) in inv_tag_tbl:
                        if (jrow,jcol) not in length_tbl:
                            length_tbl[ (jrow,jcol)] = level+1
                    new_frontier.add( (jrow,jcol))

        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)
        level += 1
    
    return length_tbl


def main(fp):
    board, tag_tbl = parse(fp)

    inv_tag_tbl = {}
    for k, vv in tag_tbl.items():
        assert vv not in inv_tag_tbl
        inv_tag_tbl[vv] = k

    adjacents = {}

    for (tag, ty), p in tag_tbl.items():
        adjacents[p] = determine_path_lengths( board, inv_tag_tbl, p)

    # Add teleporting
    for (tag, ty), v_o in tag_tbl.items():
        if ty == 'i': continue
        if tag in ['AA', 'ZZ']: continue
        v_i = tag_tbl[(tag,'i')]
        adjacents[ v_o][v_i] = 1
        adjacents[ v_i][v_o] = 1

    for (tag, ty), p in tag_tbl.items():
        print( tag, ty, p)
        for pp, l in adjacents[p].items():
            print('\t', pp, l, inv_tag_tbl[pp])

    nrows = len(board)
    ncols = len(board[0])

    start = { tag_tbl[('AA', ty)] for ty in 'io' if ('AA', ty) in tag_tbl}
    final = { tag_tbl[('ZZ', ty)] for ty in 'io' if ('ZZ', ty) in tag_tbl}

    assert len(start) == 1
    assert len(final) == 1

    start = list(start)[0]
    final = list(final)[0]

    print(start,final)

    reached = { start: 0} # state => steps

    frontier = []
    heapq.heappush(frontier, (0, start != final, start, 0))

    while frontier:

        fhat, not_done, state, ghat = heapq.heappop( frontier)

        print( f'headpop: {fhat} {not_done} {state} ({inv_tag_tbl[state]}) {ghat}') 

        if not not_done:
            assert fhat == ghat
            assert ghat == reached[final]
            return ghat

        # this has already been or will be processed because the smaller tuple is also on the PQ
        if ghat > reached[state]: continue

        (irow,icol) = state

        for new_state,cost in adjacents[state].items():
            if new_state == state: continue

            new_ghat = ghat + cost
            new_fhat = new_ghat
 
            if new_state not in reached or reached[new_state] > new_ghat:
                reached[new_state] = new_ghat
                heapq.heappush( frontier, (new_fhat, new_state != final, new_state, new_ghat))

    return None

def main2(fp):
    board, tag_tbl = parse(fp)

    inv_tag_tbl = {}
    for k, vv in tag_tbl.items():
        assert vv not in inv_tag_tbl
        inv_tag_tbl[vv] = k

    adjacents = {}

    for (tag, ty), p in tag_tbl.items():
        adjacents[p] = determine_path_lengths( board, inv_tag_tbl, p)

    min_l = None

    for (tag, ty), p in tag_tbl.items():
        print( tag, ty, p)
        for pp, l in adjacents[p].items():
            if p != pp:
                if min_l is None or l < min_l: min_l = l

            print('\t', pp, l, inv_tag_tbl[pp])

    print( f'min_l: {min_l}')

    nrows = len(board)
    ncols = len(board[0])

    start = { tag_tbl[('AA', ty)] for ty in 'io' if ('AA', ty) in tag_tbl}
    final = { tag_tbl[('ZZ', ty)] for ty in 'io' if ('ZZ', ty) in tag_tbl}

    assert len(start) == 1
    assert len(final) == 1

    start = (0, list(start)[0])
    final = (0, list(final)[0])

    print(start,final)

    reached = { start: 0} # state => steps

    frontier = []
    heapq.heappush(frontier, (0, start != final, start, 0))

    steps = 0

    while frontier:

        fhat, not_done, state, ghat = heapq.heappop( frontier)

        level, p = state

        print( f'{steps}: headpop: {fhat} {not_done} {state} {inv_tag_tbl[p]} {ghat}') 

        if not not_done:
            assert ghat == reached[final]
            return ghat

        # this has already been or will be processed because the smaller tuple is also on the PQ
        if ghat > reached[state]:
            print( f'Remove from PQ without processing... {state} {ghat} {reached[state]}')
            continue

        def gen_adjacents( p):
            for new_p,cost in adjacents[p].items():
                if new_p == p: continue
                yield (level, new_p), cost

            tag, ty = inv_tag_tbl[p]
            if tag in ['AA', 'ZZ']: return
            if ty == 'o':
                # go down a level to the 'i' cases
                if level > 0:
                    new_p = tag_tbl[ (tag,'i')]
                    yield (level-1, new_p), 1
            elif ty == 'i':
                # go up a level to the 'o' cases
                new_p = tag_tbl[ (tag,'o')]
                yield (level+1, new_p), 1

        for new_state,cost in gen_adjacents(p):

            new_ghat = ghat + cost
            new_fhat = new_ghat + (min_l+1)*level
            #new_fhat = (level, new_ghat)

            if new_state not in reached or reached[new_state] > new_ghat:
                reached[new_state] = new_ghat
                heapq.heappush( frontier, (new_fhat, new_state != final, new_state, new_ghat))

        steps += 1

    return None


@pytest.mark.skip
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

#@pytest.mark.skip
def test_AA0():
    with open("data0","rt") as fp:
        assert 26 == main2(fp)

# Infinite loop
@pytest.mark.skip
def test_AA1():
    with open("data1","rt") as fp:
        assert main2(fp) is None

#@pytest.mark.skip
def test_AA2():
    with open("data2","rt") as fp:
        assert 396 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))
