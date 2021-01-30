import pytest
import io
import re
import itertools

def parse(fp):

    seq = []

    p = re.compile( r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')

    for idx,line in enumerate(fp):
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( tuple([int(x) for x in m.groups()]))
        assert seq[-1][0] == idx+1

    return seq


def main(fp):
    seq = parse(fp)
    print(seq)

    tbl = {}
    for idx, ox, oy, sx, sy in seq:
        for x in range(ox, ox+sx):
            for y in range(oy, oy+sy):
                p = (x,y)
                if p not in tbl: tbl[p] = []
                tbl[p].append(idx)

    count = 0
    for k,v in tbl.items():
        if len(v) > 1:
            count += 1

    return count

def main2(fp):
    seq = parse(fp)

    tbl = {}
    for idx, ox, oy, sx, sy in seq:
        for p in itertools.product( range(ox, ox+sx), range(oy, oy+sy)):
            if p not in tbl: tbl[p] = []
            tbl[p].append(idx)

    okay_indices = []
    for idx, ox, oy, sx, sy in seq:
        okay = True
        for p in itertools.product( range(ox, ox+sx), range(oy, oy+sy)):
            if len(tbl[p]) > 1:
                okay = False
                break
        if okay:
            okay_indices.append(idx)
                    
    assert len(okay_indices) == 1

    return okay_indices[0]

@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 4 == main(fp)

@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA():
    with open('data0', 'rt') as fp:
        assert 3 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))
