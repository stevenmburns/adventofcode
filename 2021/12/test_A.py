from functools import reduce
import pytest, re
from collections import defaultdict

def parse(fp):
    p = re.compile(r'^(.*)\-(.*)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        yield m.groups()


def main(fp):
    data = list(parse(fp))

    adj = defaultdict(list)
    for a, b in data:
        adj[a].append(b)
        adj[b].append(a)

    large = {k for k in adj.keys() if k.upper() == k}
    small = {k for k in adj.keys() if k.lower() == k}

    assert len(large) + len(small) == len(adj)

    def dfs(u, path, small_on_path):
        if u == 'end':
            yield path
            return
        for v in adj[u]:
            if v not in small_on_path:
                yield from dfs(v, path + [v], small_on_path.union({v} if v in small else set()))

    paths = list(dfs('start', ['start'], {'start'}))
    return len(paths)



def main2(fp):
    data = list(parse(fp))

    adj = defaultdict(list)
    for a, b in data:
        adj[a].append(b)
        adj[b].append(a)

    large = {k for k in adj.keys() if k.upper() == k}
    small = {k for k in adj.keys() if k.lower() == k}

    assert len(large) + len(small) == len(adj)

    def dfs(u, path, small_on_path, small_on_path_twice):
        if u == 'end':
            #print(','.join(path))
            yield path
            return
        for v in adj[u]:
            if v not in small_on_path_twice:
                next_small_on_path = small_on_path
                next_small_on_path_twice = small_on_path_twice

                if v in small:
                    if v in small_on_path:
                        next_small_on_path_twice = small_on_path_twice.union({v})
                    else:
                        next_small_on_path = small_on_path.union({v})

                if len(next_small_on_path_twice.difference({'start'})) <= 1:
                    yield from dfs(v, path + [v], next_small_on_path, next_small_on_path_twice)

    paths = list(dfs('start', ['start'], {'start'}, {'start'}))
    return len(paths)

def test_A0():
    with open('data0') as fp:
        assert 10 == main(fp)

#@pytest.mark.skip        
def test_A1():
    with open('data1') as fp:
        assert 19 == main(fp)

#@pytest.mark.skip
def test_A2():
    with open('data2') as fp:
        assert 226 == main(fp)

#@pytest.mark.skip
def test_B():
    with open('data') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA0():
    with open('data0') as fp:
        assert 36 == main2(fp)

#@pytest.mark.skip
def test_AA1():
    with open('data1') as fp:
        assert 103 == main2(fp)

#@pytest.mark.skip
def test_AA2():
    with open('data2') as fp:
        assert 3509 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open('data') as fp:
        print(main2(fp))
