import pytest
import io
import re
import itertools

def parse(fp):

    seq = []

    p = re.compile( r'^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (wakes up|falls asleep|Guard #(\d+) begins shift)$')

    
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        tag = m.groups()[5]
        nums = tuple( [int(x) for x in m.groups()[0:5]])
        if tag.startswith('Guard'): 
            seq.append( (nums, 0, int(m.groups()[6])))
        elif tag.startswith('falls'):
            seq.append( (nums, 1, None))
        elif tag.startswith('wakes'):
            seq.append( (nums, 2, None))
        else:
            assert False, tag

        assert m, line



    seq.sort()


    guard_id = None
    guard_list = []

    new_seq = []

    for tup in seq:
        nums, state, guard = tup
        if state == 0:
            if guard_id is not None:
                new_seq.append( (guard_id, guard_list))
            guard_id = guard
            guard_list = [(0,nums)]
        elif state == 1:
            assert guard_id is not None, tup
            assert guard_list[-1][0] in [0,2]
            guard_list.append( (1,nums))
        elif state == 2:
            assert guard_id is not None, tup
            assert guard_list[-1][0] in [1]
            guard_list.append( (2,nums))
        else:
            assert False, state

    if guard_id is not None:
        new_seq.append( (guard_id, guard_list))

    return new_seq

from collections import defaultdict

def main(fp):
    new_seq = parse(fp)
    print(new_seq)

    sleeping_minutes = defaultdict(int)

    raster = {}

    for guard, lst in new_seq:
        assert len(lst) % 2 == 1
        for idx in range(1,len(lst),2):
            state1, num1 = lst[idx]
            assert state1 == 1
            state2, num2 = lst[idx+1]
            assert state2 == 2
            _, _, dy1, hr1, mn1 = num1
            _, _, dy2, hr2, mn2 = num2
            assert dy1 == dy2
            assert hr1 == hr2 == 0
            assert mn2 >= mn1
            
            sleeping_minutes[guard] += mn2 - mn1
            
            for i in range(mn1,mn2):
                if guard not in raster:
                    raster[guard] = defaultdict(int)
                raster[guard][i] += 1

    M = max( [v for k, v in sleeping_minutes.items()])
    most_sleepy_guards = { k for k,v in sleeping_minutes.items() if v == M}
    print(most_sleepy_guards)

    assert len(most_sleepy_guards) == 1

    g = list(most_sleepy_guards)[0]

    M = max( [v for k, v in raster[g].items()])
    best_hours = { k for k,v in raster[g].items() if v == M}

    assert len(best_hours) == 1

    h = list(best_hours)[0]

    return g*h

def main2(fp):
    new_seq = parse(fp)
    print(new_seq)

    sleeping_minutes = defaultdict(int)

    raster = {}

    for guard, lst in new_seq:
        assert len(lst) % 2 == 1
        for idx in range(1,len(lst),2):
            state1, num1 = lst[idx]
            assert state1 == 1
            state2, num2 = lst[idx+1]
            assert state2 == 2
            _, _, dy1, hr1, mn1 = num1
            _, _, dy2, hr2, mn2 = num2
            assert dy1 == dy2
            assert hr1 == hr2 == 0
            assert mn2 >= mn1
            
            sleeping_minutes[guard] += mn2 - mn1
            
            for i in range(mn1,mn2):
                if guard not in raster:
                    raster[guard] = defaultdict(int)
                raster[guard][i] += 1



    tuples = []
    for g in raster.keys():
        M = max( [v for k, v in raster[g].items()])
        tuples.append( (g, M, { k for k,v in raster[g].items() if v == M}))
        
    tuples.sort(key=lambda p: p[1])

    g = tuples[-1][0]
    h = list(tuples[-1][2])[0]

    print( tuples)


    return g*h

@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 240 == main(fp)

@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AA():
    with open('data0', 'rt') as fp:
        assert 4455 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))
