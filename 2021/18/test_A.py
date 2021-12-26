import re, pytest, io
from copy import deepcopy

def parse(fp):
    p = re.compile(r'^(\d|\,|\[|\])*$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        yield eval(line)

def magnitude(lst):
    if type(lst) == int:
        return lst
    else:
        a, b = lst
        return 3*magnitude(a) + 2*magnitude(b)

def depth(lst):
    if type(lst) == int:
        return -1, ()
    else:
        a, b = lst
        da, pa = depth(a)
        db, pb = depth(b)
        return 1 + max(da,db), (0,) + pa if da >= db else (1,) + pb
    
def left_most_regular_number_greater_than_or_equal_to_10(lst):
    if type(lst) == int:
        return () if lst >= 10 else None
    else:
        a, b = lst
        pa = left_most_regular_number_greater_than_or_equal_to_10(a)
        pb = left_most_regular_number_greater_than_or_equal_to_10(b)
        if pa is not None:
            return (0,) + pa
        elif pb is not None:
            return (1,) + pb
        else:
            return None

def all_paths(lst):
    paths = []
    def aux(pair, path):
        if type(pair) == int:
            paths.append(path)
        else:
            [l, r] = pair
            aux(l, path + (0,))
            aux(r, path + (1,))

    aux(lst, ())
    return paths

def find_element(lst, p):
    pair = lst
    for x in p:
        pair = pair[x]
    return pair

def find_element_reference(lst, p):
    pair, prev_pair = lst, None
    for x in p:
        pair, prev_pair = pair[x], pair
    return pair, prev_pair, p[-1]

def test_all_paths():
    lst = [[[0,1],[2,3]],4]
    paths = all_paths(lst)
    for idx, path in enumerate(paths):
        el = find_element(lst, path)
        el0, prev_pair, which = find_element_reference(lst, path)
        assert el0 == el 
        assert prev_pair[which] == el0
        assert el == idx

def explode(lst, p):
    paths = all_paths(lst)
    left_of = None
    right_of = None
    prev = None
    lp, rp = p[:-1] + (0,), p[:-1] + (1,)
    for path in paths:
        if prev == rp:
            right_of = path
        if path == lp:
            left_of = prev
        prev = path
    assert p in paths
    assert len(p) == 5

    (add_left, add_right), save_prev_pair, save_which = find_element_reference(lst, p[:-1])

    if left_of is not None:
        _, prev_pair, which = find_element_reference(lst, left_of)
        prev_pair[which] += add_left

    if right_of is not None:
        _, prev_pair, which = find_element_reference(lst, right_of)
        prev_pair[which] += add_right

    save_prev_pair[save_which] = 0

    return lst

def test_explode0():
    res = [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
    d, p = depth(res)
    assert d == 4
    res = explode(res, p)
    assert res == [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
    d, p = depth(res)
    assert d == 4
    res = explode(res, p)
    assert res == [[[[0,7],4],[15,[0,13]]],[1,1]]

def split(lst, p):

    def split_pair(x):
        return [x//2, (x+1)//2]
    sublst = lst
    if p == ():
        return split_pair(lst)

    for i in p[:-1]:
        sublst = sublst[i]

    i = p[-1]

    sublst[i] = split_pair(sublst[i])

    return lst

def test_split0():
    res = [[[[0,7],4],[15,[0,13]]],[1,1]]
    p = left_most_regular_number_greater_than_or_equal_to_10(res)
    res = split(res, p)
    assert res == [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
    p = left_most_regular_number_greater_than_or_equal_to_10(res)
    res = split(res, p)
    assert res == [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]

def reduce(res):
    while True:
        d, p = depth(res)
        assert d <= 4

        if d == 4:
            res = explode(res, p)
        else:
            p = left_most_regular_number_greater_than_or_equal_to_10(res)
            if p is None:
                break
            else:
                res = split(res, p)

    return res

def add(u, v):
    assert depth(u)[0] < 4
    assert depth(v)[0] < 4

    res = [u, v]
    res = deepcopy(res)
    return reduce(res)

def addlist(trees):
    u = trees[0]

    for v in trees[1:]:
        u = add(u, v)   

    return u 

def test_addlist0():
    assert addlist( [
        [1,1],
        [2,2],
        [3,3],
        [4,4]
    ]) == [[[[1,1],[2,2]],[3,3]],[4,4]]

def test_addlist1():
    assert addlist( [
        [1,1],
        [2,2],
        [3,3],
        [4,4],
        [5,5]
    ]) == [[[[3,0],[5,3]],[4,4]],[5,5]]

def test_addlist2():
    assert addlist( [
        [1,1],
        [2,2],
        [3,3],
        [4,4],
        [5,5],
        [6,6]
    ]) == [[[[5,0],[7,4]],[5,5]],[6,6]]

@pytest.mark.skip
def test_addlist3():
    assert addlist( [
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
[7,[5,[[3,8],[1,4]]]],
[[2,[2,2]],[8,[8,1]]],
[2,9],
[1,[[[9,3],9],[[9,0],[0,7]]]],
[[[5,[7,4]],7],1],
[[[[4,2],2],6],[8,7]],
    ]) == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] 
    

def test_add0():
    assert add(
        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    ) == [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]


def main(fp):
    trees = list(parse(fp))
    u = addlist(trees)
    return magnitude(u)

def main2(fp):
    trees = list(parse(fp))
    M = 0, 0, 0
    for i in range(len(trees)):
        for j in range(len(trees)):
            if i == j:
                continue
            cand = magnitude(add( trees[i], trees[j]))
            tup = cand,i,j
            M = max(M, tup)

    return M[0]

#@pytest.mark.skip
def test_A0():
    with open('data0', 'rt') as fp:
        assert 4140 == main(fp)

def test_magnitude():
    assert 143 == magnitude([[1,2],[[3,4],5]])
    assert 1384 == magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
    assert 4140 == magnitude([[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]])

#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        assert 3869 == main(fp)

#@pytest.mark.skip
def test_AA():
    with open('data0', 'rt') as fp:
        assert 3993 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))