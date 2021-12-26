import re, pytest

from itertools import combinations, product
from collections import defaultdict

def parse(fp):
    p0 = re.compile(r'^--- scanner (\d+) ---$')
    p_blank = re.compile(r'^\s*$')
    p = re.compile(r'^((|-)\d+),((|-)\d+),((|-)\d+)$')

    scanner = None
    positions = []
    for line in fp:
        line = line.rstrip('\n')
        m = p0.match(line)
        if m:
            assert scanner is None
            scanner = int(m.groups()[0])
            continue
        m = p_blank.match(line)
        if m:
            assert scanner is not None
            yield scanner, positions
            scanner = None
            positions = []
            continue
        m = p.match(line)
        if m:
            positions.append( (int(m.groups()[0]), int(m.groups()[2]), int(m.groups()[4])) )
            continue
        assert False, line

    if scanner is not None:
        yield scanner, positions

class Transformation:
    def __init__(self):
        self.A = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]

    @staticmethod
    def translate(tx, ty, tz):
        res = Transformation()
        res.A[0][3] = tx
        res.A[1][3] = ty
        res.A[2][3] = tz
        return res


    @staticmethod
    def rotate_z_90():
        res = Transformation()
        res.A = [[0,-1,0,0], [1,0,0,0], [0,0,1,0], [0,0,0,1]]
        return res

    @staticmethod
    def rotate_x_90():
        res = Transformation()
        res.A = [[1,0,0,0], [0,0,-1,0], [0,1,0,0], [0,0,0,1]]
        return res

    @staticmethod
    def fromTuple(t):
        res = Transformation()
        for i in range(4):
            for j in range(4):
                res.A[i][j] = t[i][j]
        return res

    def __repr__(self):
        return f'Transformation(A={self.A})'

    def toTuple(self):
        return tuple(tuple(row) for row in self.A)

    def _hit(self, v):
        return tuple(sum(self.A[i][j]*v[j] for j in range(4)) for i in range(4))

    def hit(self, v):
        return self._hit(v + (1,))[:3]

    @staticmethod
    def sub(a, b):
        return tuple(aa - bb for aa,bb in zip(a,b))

    @staticmethod
    def mul(a, b):
        result = Transformation()
        for i in range(4):
            for j in range(4):
                result.A[i][j] = 0
                for k in range(4):
                    result.A[i][j] += a.A[i][k] * b.A[k][j]
        return result

    def preMult(self, other):
        return Transformation.mul(other, self)

    def postMult(self, other):
        return Transformation.mul(self, other)

    def transpose(self):
        return Transformation.fromTuple(tuple(tuple(row[i] for row in self.A) for i in range(4)))

    def inverse(self):
        t = Transformation.translate(-self.A[0][3], -self.A[1][3], -self.A[2][3])
        res = self.preMult(t).transpose().postMult(t)
        assert self.postMult(res).A == Transformation().A
        assert self.preMult(res).A == Transformation().A
        return res



def gen_rotations():
    rz = Transformation.rotate_z_90()
    rx = Transformation.rotate_x_90()

    frontier = {Transformation().toTuple()}

    reachable = set()

    while frontier:
        newfrontier = set()
        for t in frontier:
            for r in [rz, rx]:
                newfrontier.add(Transformation().fromTuple(t).postMult(r).toTuple())

        reachable.update(frontier)

        frontier = newfrontier.difference(reachable)

    assert len(reachable) == 24

    return [Transformation.fromTuple(t) for t in reachable]    


def test_inverses():
    rotations = gen_rotations()
    inverses = []

    for rot in rotations:
        for inv_rot in rotations:
            if rot.postMult(inv_rot).toTuple() == Transformation().toTuple():
                inverses.append(inv_rot)
                break
    assert len(rotations) == len(inverses)

    for rot, inv in zip(rotations, inverses):
        assert rot.inverse().A == inv.A

def main(fp):
    reports = list(parse(fp))

    rotations = gen_rotations()

    matches = []
    for (ia, a), (ib, b) in combinations(reports, 2):

        for rot in rotations:
            tbl = defaultdict(list)
            for iaa, aa in enumerate(a):
                for ibb, bb in enumerate(b):
                    diff = Transformation.sub(aa, rot.hit(bb))
                    tbl[diff].append((iaa, ibb))

            for diff, hits in tbl.items():
                if len(hits) >= 12:
                    matches.append((ia, ib, rot, diff, hits))


    a_dict = { ia : a for ia, a in reports}
    b_dict = { ib : b for ib, b in reports}

    edge_info = {}

    for ia, ib, rot, diff, hits in matches:

        res = Transformation.translate(*diff).postMult(rot)

        a, b = a_dict[ia], b_dict[ib]

        for iaa, ibb in hits:
            aa, bb = a[iaa], b[ibb]

            assert res.hit(bb) == aa

        edge_info[(ia, ib)] = (res, hits)

    for ia, ib, rot, diff, hits in matches:

        res = Transformation.translate(*diff).postMult(rot).inverse()
        invhits = [(ibb, iaa) for iaa, ibb in hits]

        a, b = a_dict[ia], b_dict[ib]

        for iaa, ibb in hits:
            aa, bb = a[iaa], b[ibb]

            assert res.hit(aa) == bb

        edge_info[(ib, ia)] = (res, invhits)


    edges = defaultdict(list)
    for ia, ib, _, _, _ in matches:
        edges[ia].append(ib)
        edges[ib].append(ia)

    visited = set()
    tr_dict = {}


    def dfs(u, tr):
        visited.add(u)
        tr_dict[u] = tr
        for v in edges[u]:
            if v not in visited:
                dfs(v, tr.postMult(edge_info[(u, v)][0]))

    dfs(0, Transformation())

    print(visited, tr_dict)

    scanner_positions = {}

    beacons = set()
    for ia, a in reports:
        if ia not in tr_dict:
            continue
        tr = tr_dict[ia]
        scanner_pos = tr.A[0][3], tr.A[1][3], tr.A[2][3]
        scanner_positions[ia] = scanner_pos
        for iaa, aa in enumerate(a):
            beacon_pos = tr.hit(aa)
            assert all(abs(p-q) <= 1000 for p,q in zip(beacon_pos, scanner_pos))
            beacons.add(beacon_pos)

    M = 0
    for ispa, ispb in combinations(list(scanner_positions.keys()), 2):
        M = max(M, sum(abs(p-q) for p,q in zip(scanner_positions[ispa], scanner_positions[ispb])))

    return len(beacons), M

def main2(fp):
    ...

#@pytest.mark.skip
def test_A0():
    with open('data0', 'rt') as fp:
        assert (79, 3621) == main(fp)

#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))
