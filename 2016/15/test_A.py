import pytest
import io
import re
import hashlib
from math import gcd

def parse(fp):
    seq = []

    p = re.compile(r'^Disc #(\d+) has (\d+) positions; at time=(\d+), it is at position (\d+).$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( (int(m.groups()[0]),int(m.groups()[1]),int(m.groups()[2]),int(m.groups()[3])))
        
    return seq

def lcm( lst):
    result = 1
    for x in lst:
        result = result*x//gcd(result,x)
    return result

def main(fp):
    seq = parse(fp)
    print(seq)

    period = lcm( tup[1] for tup in seq)
    print( f'period: {period}')

    for time in range(period):
        all_open = True
        for disc in seq:
            (disc_num, disc_period, disc_start, disc_pos) = disc
            assert disc_start == 0
            current_disc_pos = (time + disc_num + disc_pos) % disc_period
            if current_disc_pos != 0:
                all_open = False
        if all_open:
            return time
            break

    return None

def main2(fp):
    seq = parse(fp)


    seq.append( (seq[-1][0]+1, 11, 0, 0))
    print(seq)

    period = lcm( tup[1] for tup in seq)
    print( f'period: {period}')

    for time in range(period):
        all_open = True
        for disc in seq:
            (disc_num, disc_period, disc_start, disc_pos) = disc
            assert disc_start == 0
            current_disc_pos = (time + disc_num + disc_pos) % disc_period
            if current_disc_pos != 0:
                all_open = False
        if all_open:
            return time
            break

    return None



def test_A():
    with open("data0","rt") as fp:
        assert 5 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))
    with open("data","rt") as fp:
        print(main2(fp))

