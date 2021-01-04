import io
import re

def parse(fp):

    seq = []

    p = re.compile(r'^([UDRL]+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( line)

    return seq

keypad1 = { (0,0): '1', (0,1): '2',  (0,2): '3', 
            (1,0): '4', (1,1): '5',  (1,2): '6', 
            (2,0): '7', (2,1): '8',  (2,2): '9'}

keypad2 = {                        (0,2): '1', 
                       (1,1): '2', (1,2): '3', (1,3): '4', 
           (2,0): '5', (2,1): '6', (2,2): '7', (2,3): '8',  (2,4): '9', 
                       (3,1): 'A', (3,2): 'B', (3,3): 'C', 
                                   (4,2): 'D'}

deltas = { 'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}

def step( p, c, keypad):
    irow,icol = p

    drow,dcol = deltas[c]

    jrow,jcol = irow+drow,icol+dcol

    if (jrow,jcol) in keypad:
        return jrow,jcol
    else:
        return p


def main(fp,start=(1,1),keypad=keypad1):
    seq = parse(fp)
    print(seq)

    code = []
    p = start
    for s in seq:
        for c in s:
            p = step( p, c, keypad)
        code.append( keypad[p])

    return ''.join( code)

def test_A():
    with open( "data0", "rt") as fp:
        assert '1985' == main(fp)
    with open( "data0", "rt") as fp:
        assert '5DB3' == main(fp,start=(2,0),keypad=keypad2)

def test_B():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main(fp,start=(2,0),keypad=keypad2))
