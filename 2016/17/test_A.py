import pytest
import io
import re
import hashlib
from collections import deque

dirs = [ ('U',(-1,0)), ('D',(1,0)), ('L',(0,-1)), ('R',(0,1))]
def gen_neighbors( txt, state):
    (irow, icol), path = state
    if irow == 3 and icol == 3: return
    base = f'{txt}{path}'
    hexstr = hashlib.md5(base.encode()).hexdigest()
    open_doors = [ c in 'bcdef' for c in hexstr[:4]]
    for idx in range(len(dirs)):
        (drow,dcol) = dirs[idx][1]
        jrow, jcol = irow+drow, icol+dcol
        if open_doors[idx] and 0 <= jrow < 4 and 0 <= jcol < 4:
            yield ((jrow, jcol), path + dirs[idx][0])

def main(txt):
    init_state = ((0,0), '')

    q = deque()
    q.append(init_state)
    while q:
        state = q.popleft()
        ((irow,icol),path) = state
        if irow == 3 and icol == 3:
            return path
        for next_state in gen_neighbors(txt,state):
            q.append(next_state)

    return None

def main2(txt):
    init_state = ((0,0), '')

    q = deque()
    q.append(init_state)
    longest_path = None
    while q:
        state = q.popleft()
        ((irow,icol),path) = state
        if irow == 3 and icol == 3:
            if longest_path is None or len(path) > longest_path:
                longest_path = len(path)
        for next_state in gen_neighbors(txt,state):
            q.append(next_state)

    return longest_path

def test_A0():
    assert 'DDRRRD' == main('ihgpwlah')
def test_A1():
    assert 'DDUDRLRRUDRD' == main('kglvqrro')
def test_A2():
    assert 'DRURDRUDDLLDLUURRDULRLDUUDDDRR' == main('ulqzkmiv')

def test_AA0():
    assert 370 == main2('ihgpwlah')
def test_AA1():
    assert 492 == main2('kglvqrro')
def test_AA2():
    assert 830 == main2('ulqzkmiv')

def test_B():
    print( main('udskfozm'))
def test_BB():
    print( main2('udskfozm'))

