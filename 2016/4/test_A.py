import pytest
import io
import re

def parse(fp):

    seq = []

    p = re.compile(r'^([0-9a-z\-]+)\[([a-z]+)\]$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m

        q = m.groups()[0].split('-')

        seq.append( (q[:-1],int(q[-1]), m.groups()[1]))

    return seq


def is_real_room( triple):
    nm, id, checksum = triple
    
    histo = {}
    for word in nm:
        for c in word:
            if c not in histo:
                histo[c] = 0
            histo[c] += 1

    lst = [ (-v,k) for (k,v) in histo.items()]
    lst.sort()

    new_checksum = ''
    for (idx,(count,c)) in enumerate(lst):
        if idx < 5:
            new_checksum += c

    if checksum == new_checksum:
        return True, id
    else:
        return False, None

def main(fp):
    seq = parse(fp)
    count = 0
    for triple in seq:
        valid, id = is_real_room( triple)
        if valid:
            count += id

    return count

def main2(fp):
    seq = parse(fp)
    for triple in seq:
        valid, id = is_real_room( triple)
        if valid:
            nm, id, checksum = triple
            new_nm = []
            for word in nm:
                new_word = ''
                for c in word:
                    new_c = chr((ord(c)-ord('a')+id)%26+ord('a'))
                    new_word += new_c
                new_nm.append(new_word)
            message = ' '.join(new_nm)
            if message == 'northpole object storage':
                return id
    return None

def test_A():
    with open( "data0", "rt") as fp:
        assert 1514 == main(fp)

def test_B():
    with open( "data", "rt") as fp:
        print(main(fp))
    with open( "data", "rt") as fp:
        print(main2(fp))
