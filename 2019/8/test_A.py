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
        seq.append( line)

    assert len(seq) == 1

    return seq[0]

def main(fp):
    s = parse(fp)

    w = 25
    h = 6

    layers = []
    rows = []
    row = ''
    for c in s:
        row += c
        if len(row) == w:
            rows.append( row)
            row = ''
            if len(rows) == h:
                layers.append(rows)
                rows = []
        
    assert not rows and not row

    print( f'Number of layers {len(layers)}')

    metrics = []
    for rows in layers:
        histo = defaultdict(int)
        for row in rows:
            for c in row:
                histo[c] += 1
        print( histo)
        metrics.append( (histo['0'], histo['1']*histo['2']))

    metrics.sort()

    print( f'Checksum {metrics[0][1]}')

    result = [ [ '2' for _ in range(w)] for _ in range(h)]

    for rows in reversed(layers):
        for irow, row in enumerate(rows):
            for icol, c in enumerate(row):
                if c in '01':
                    result[irow][icol] = c

    print()
    for row in result:
        print( ''.join( c if c == '1' else ' ' for c in row))

    return 0


#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))



