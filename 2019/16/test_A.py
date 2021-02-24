import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging
import time

#logging.basicConfig(level=logging.INFO)

def clean( x):
    return abs(x)%10

def pattern( n, r):
    base_pattern = [0,1,0,-1]

    result = []
    j = 0
    for i in range(1,n+2):
        result.append(base_pattern[j])
        if i % r == (r-1):
            j = (j+1) % len(base_pattern)
    if r == 1:
        return result[1:]
    else:
        return result[:-1]

def pattern_rle( n, r):
    if r == 1:
        return run_length_encode( pattern( n, r), 0)

    base_pattern = [0,1,0,-1]

    result = []

    i = 0
    j = 0
    start = 0
    c = base_pattern[0]
    i = r-1
    while i < n:
        if base_pattern[j] != 0:
            result.append( (start,i,base_pattern[j]))
        j = (j+1) % len(base_pattern)        
        start = i
        i += r

    if start < n:
        if base_pattern[j] != 0:
            result.append( (start,n,base_pattern[j]))

    return result



def inner( pat, lst):
    #print( ''.join( '-' if x < 0 else ('+' if x > 0 else '0') for x in pat))
    #print( ''.join( str(x) for x in lst))
    return sum( x*y for x,y in zip(pat,lst))

def run_length_encode( pat, zero):
    start = None
    current = None
    tuples = []
    for idx, c in enumerate(pat):
        if start is None:
            start = idx
            current = c
        elif current == c:
            pass
        else:
            if current != zero:
                tuples.append( (start,idx,current))
            start = idx
            current = c

    if current != zero:
        tuples.append( (start,len(pat),current))

    return tuples

def test_run_length_encode0():
    pat = '0011000111'
    assert [ (2,4,'1'), (7, 10, '1')] == run_length_encode( pat, '0')

def test_run_length_encode1():
    pat = '--++---+++'
    assert [ (0,2,'-'), (2,4,'+'), (4,7,'-'), (7,10,'+')] == run_length_encode( pat, '0')


def compressed_inner( pat_rle, cummulative_lst):
    s = 0
    for (start,end,coeff) in pat_rle:
        s += coeff* (cummulative_lst[end]-cummulative_lst[start])
    return s

def cummulative_sum( lst):
    s = 0
    result = [s]
    for x in lst:
        s += x
        result.append(s)
    return result


def inner2( pat, lst):
    return compressed_inner( run_length_encode( pat, 0), cummulative_sum( lst))

def main(s,iters,repeat=1,offset=0):

    lst = [ int(c) for c in s]

    lst = lst*repeat

    start = time.monotonic()
    last = start
    for iter in range(iters):
        cummulative_lst = cummulative_sum( lst)
        new_lst = []
        for idx in range(len(lst)):
            if idx % 1000 == 0:
                print(idx)
            if False:
                pat = pattern( len(lst), idx+1)
                value = inner( pat, lst)
            else:
                #pat = pattern( len(lst), idx+1)                
                #pat_rle = run_length_encode( pat, 0)
                pat_rle = pattern_rle( len(lst), idx+1)
                value = compressed_inner( pat_rle, cummulative_lst)
            new_lst.append( clean( value))
        lst = new_lst
        end = time.monotonic()
        print( f'Iteration {iter} {end-start} {end-last}')
        last = end

        
    return ''.join( str(x) for x in lst[offset:offset+8])


@pytest.mark.skip
def test_A0():
    assert '01029498' == main( '12345678', 4)

@pytest.mark.skip
def test_A1():
    assert '24176176' == main( '80871224585914546619083218645595', 100)

@pytest.mark.skip
def test_A2():
    assert '73745418' == main( '19617804207202209144916044189917', 100)

@pytest.mark.skip
def test_A3():
    assert '52432133' == main( '69317163492948606335995924319873', 100)

@pytest.mark.skip
def test_B():
    print(main('59740570066545297251154825435366340213217767560317431249230856126186684853914890740372813900333546650470120212696679073532070321905251098818938842748495771795700430939051767095353191994848143745556802800558539768000823464027739836197374419471170658410058272015907933865039230664448382679990256536462904281204159189130560932257840180904440715926277456416159792346144565015659158009309198333360851441615766440174908079262585930515201551023564548297813812053697661866316093326224437533276374827798775284521047531812721015476676752881281681617831848489744836944748112121951295833143568224473778646284752636203058705797036682752546769318376384677548240590',100))

#@pytest.mark.skip
def test_BB():
    s = '59740570066545297251154825435366340213217767560317431249230856126186684853914890740372813900333546650470120212696679073532070321905251098818938842748495771795700430939051767095353191994848143745556802800558539768000823464027739836197374419471170658410058272015907933865039230664448382679990256536462904281204159189130560932257840180904440715926277456416159792346144565015659158009309198333360851441615766440174908079262585930515201551023564548297813812053697661866316093326224437533276374827798775284521047531812721015476676752881281681617831848489744836944748112121951295833143568224473778646284752636203058705797036682752546769318376384677548240590'

    offset = int(s[:7])

    print(main(s,100,10000,offset))




