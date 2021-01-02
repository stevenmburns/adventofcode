
import io

import logging
from logging import debug
import re

logging.basicConfig(level=logging.DEBUG)

def gen_id(s):
    assert len(s) == 10

    id = 0
    for i in range(10):
        if s[9-i] in ["R","B"]:
            id |= 1<<i

    return id

def main( fp):
    debug("Part 1")

    max_id = -1

    for line in fp:
        line = line.rstrip('\n')
        id = gen_id(line)
        max_id = max(max_id,id)

    return max_id

def main2( fp):
    debug("Part 2")

    s = set()

    for line in fp:
        line = line.rstrip('\n')
        id = gen_id(line)
        print(id)
        s.add(id)

    print( s)

    empty_seats = []
    for i in range( 1<<10):
        if i not in s:
            empty_seats.append(i)

    print(empty_seats)

def dont_run_test_A():
    fp = io.StringIO( """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
""")

    assert 820 == main(fp)

def test_B():
    with open( "data", "rt") as fp:
        main2(fp)
    
