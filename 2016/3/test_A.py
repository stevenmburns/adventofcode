import io
import re

def parse(fp):

    seq = []

    p = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s*$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        
        seq.append( [ int(m.groups()[i]) for i in range(3)])

    return seq


def is_triangle( lst):
    lst.sort()
    return lst[0] + lst[1] > lst[2]

def main(fp):
    seq = parse(fp)
    print(seq)

    count = 0
    for lst in seq:
        if is_triangle( lst):
            count += 1

    print(seq)

    return count

def main2(fp):
    seq = parse(fp)

    new_seq = []
    for icol in range(3):
        for irow in range(0,len(seq),3):
            lst = []
            for jrow in range(irow,irow+3):
                lst.append( seq[jrow][icol])
            new_seq.append( lst)
            
    print(new_seq)

    count = 0
    for lst in new_seq:
        if is_triangle( lst):
            count += 1

    print(new_seq)

    return count

def test_B():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))
