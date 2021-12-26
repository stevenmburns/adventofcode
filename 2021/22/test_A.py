
import pytest, re
from bisect import bisect_left


def parse(fp):
    p = re.compile(r'^(on|off) x=((|-)\d+)\.\.((|-)\d+),y=((|-)\d+)\.\.((|-)\d+),z=((|-)\d+)\.\.((|-)\d+)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        yield m.groups()[0], int(m.groups()[1]), int(m.groups()[3]), int(m.groups()[5]), int(m.groups()[7]), int(m.groups()[9]), int(m.groups()[11])


def main(fp):
    s = set()
    for cmd, x1, x2, y1, y2, z1, z2 in parse(fp):
        if x1 < -50 or x2 > 50: continue
        print(cmd, x1, x2, y1, y2, z1, z2)
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                for z in range(z1, z2+1):
                    if cmd == 'on':
                        s.add((x, y, z))
                    elif cmd == 'off':
                        s.discard((x, y, z))
    return len(s)

def main2(fp):
    adjusted_cmds = [(cmd, x1, x2+1, y1, y2+1, z1, z2+1) for cmd, x1, x2, y1, y2, z1, z2 in parse(fp)]

    xs = set()
    ys = set()
    zs = set()
    for cmd, x1, x2, y1, y2, z1, z2 in adjusted_cmds:
        xs.update([x1,x2])
        ys.update([y1,y2])
        zs.update([z1,z2])

    print(len(xs), len(ys), len(zs)) 
    xx = list(sorted(xs))
    yy = list(sorted(ys))
    zz = list(sorted(zs))

    def breakup_cube(x1, x2, y1, y2, z1, z2):
        ix1, ix2 = bisect_left(xx, x1), bisect_left(xx, x2)
        iy1, iy2 = bisect_left(yy, y1), bisect_left(yy, y2)
        iz1, iz2 = bisect_left(zz, z1), bisect_left(zz, z2)
        assert xx[ix1] == x1 and xx[ix2] == x2
        assert yy[iy1] == y1 and yy[iy2] == y2
        assert zz[iz1] == z1 and zz[iz2] == z2
        for ix in range(ix1, ix2):
            for iy in range(iy1, iy2):
                for iz in range(iz1, iz2):
                    yield xx[ix], xx[ix+1], yy[iy], yy[iy+1], zz[iz], zz[iz+1]

    s = set()
    for idx, (cmd, x1, x2, y1, y2, z1, z2) in enumerate(adjusted_cmds):
        print(cmd, x1, x2, y1, y2, z1, z2, len(s), idx, len(adjusted_cmds))
        for cube in breakup_cube(x1, x2, y1, y2, z1, z2):
            if cmd == 'on':
                s.add(cube)
            elif cmd == 'off':
                s.discard(cube)

    ss = 1
    for x1, x2, y1, y2, z1, z2 in s:
        ss += (x2-x1)*(y2-y1)*(z2-z1)

    return ss

@pytest.mark.skip
def test_A0():
    with open('data0', 'rt') as fp:
        assert 39 == main(fp)

@pytest.mark.skip
def test_A1():
    with open('data1', 'rt') as fp:
        assert 590784 == main(fp)

@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA1():
    with open('data1', 'rt') as fp:
        assert 590784 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))


