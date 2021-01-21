import sys
import pytest
import io
import re
import itertools
from collections import deque

def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)

    print( [len(line) for line in seq])

    width = len(seq[0])
    assert all( len(line) == width for line in seq)

    return seq

def scan_rows( seq):
    scan_lines = []
    for (irow,row) in enumerate(seq):
        start = None
        tags = ''
        for i in range(len(row)):
            if start is not None:
                assert row[i] != ' ', (irow,start,i,row,row[i])
                if row[i] == '+':
                    scan_lines.append( ( irow, (start, i), tags))
                    start = None
                    tags = ''
                if row[i] not in '+|-':
                    tags += row[i]
            else:
                if i < 2 and row[i] not in ' |' or row[i] == '+':
                    start = i
                    if row[i] not in '+|-':
                        tags += row[i]
            assert row[i] != '-' or start is not None
    return scan_lines

def scan_cols( seq):
    scan_lines = []
    for icol in range(len(seq[0])):
        col = ''.join( seq[irow][icol] for irow in range(len(seq)))
        start = None
        tags = ''
        for i in range(len(col)):
            if start is not None:
                assert col[i] != ' ', (icol,start,i,col,col[i])
                if col[i] not in '+|-':
                    tags += col[i]
                if col[i] in '+Y':
                    scan_lines.append( ( icol, (start, i), tags))
                    start = None
                    tags = ''
            else:
                if i < 1 and col[i] not in ' ' or col[i] in '+':
                    start = i
                    if col[i] not in '+|-':
                        tags += col[i]
            assert col[i] != '|' or start is not None
    return scan_lines

def main(fp):
    seq = parse(fp)

    chars = set()
    for line in seq:
        for c in line:
            chars.add(c)
    chars = chars.difference( set('-| +'))


    scan_line_rows = scan_rows( seq)
    scan_line_cols = scan_cols( seq)

    tbl = {}
    for irow, (start,end), tags in scan_line_rows:
        sp = (irow,start)
        ep = (irow,end)
        if sp not in tbl: tbl[sp] = []
        tbl[sp].append( (sp,ep,tags))
        if ep not in tbl: tbl[ep] = []
        tbl[ep].append( (sp,ep,tags))
    for icol, (start,end), tags in scan_line_cols:
        sp = (start,icol)
        ep = (end,icol)
        if sp not in tbl: tbl[sp] = []
        tbl[sp].append( (sp,ep,tags))
        if ep not in tbl: tbl[ep] = []
        tbl[ep].append( (sp,ep,tags))

    start_or_end = set()
    for (k,v) in tbl.items():
        assert len(v) == 1 or len(v) == 2
        if len(v) == 1:
            start_or_end.add( k)

    assert len(start_or_end) == 2

    start = set()
    for (irow,icol) in start_or_end:
        if irow == 0:
            start.add( (irow,icol))

    assert len(start) == 1
    end = start_or_end.difference(start)
    assert len(end) == 1

    start = list(start)[0]
    end = list(end)[0]
    print( start, tbl[start])
    print( end, tbl[end])

    count = 0

    reached = set()
    cursor = start
    path = ''
    print(cursor,path)
    while cursor != end:
        last_cursor = cursor
        for sp,ep,tags in tbl[cursor]:
            edge = frozenset( { sp, ep})
            if edge not in reached:
                if cursor == sp:
                    cursor = ep
                    path += tags
                elif cursor == ep:
                    cursor = sp
                    path += tags[::-1]
                else:
                    assert False, (sp, ep, cursor)
                reached.add( edge)
        count += abs(cursor[0]-last_cursor[0]) + abs(cursor[1]-last_cursor[1])
        print(cursor,path)

    for k, lst in tbl.items():
        for sp, ep, tags in lst:
            if tags == 'Y':
                print( lst)
            edge = frozenset( { sp, ep})
            if edge not in reached:
                print('Edge not found', edge)

    assert len(path) == len(chars)

    return path,count+1

#@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert ('ABCDEF',38) == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))


