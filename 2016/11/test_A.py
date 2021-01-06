import pytest
import io
import re

def parse(fp):

    p_empty = re.compile(r'^The (\S+) floor contains nothing relevant\.$')
    p_one = re.compile(r'^The (\S+) floor contains a (\S+ \S+)\.$')
    p_two = re.compile(r'^The (\S+) floor contains a (\S+ \S+) and a (\S+ \S+)\.$')
    p_multi = re.compile(r'^The (\S+) floor contains( a (\S+ \S+)((, a (\S+ \S+))+), and a (\S+ \S+))\.$')

    seq = []

    for line in fp:
        line = line.rstrip('\n')
        print(line)
        m = p_empty.match(line)
        if m:
            seq.append( (m.groups()[0], []))
            continue
        m = p_one.match(line)
        if m:
            seq.append( (m.groups()[0], [m.groups()[1]]))
            continue
        m = p_two.match(line)
        if m:
            seq.append( (m.groups()[0], [m.groups()[1],m.groups()[2]]))
            continue
        m = p_multi.match(line)
        if m:
            s = m.groups()[1].replace('and ','').split(',')
            s = [ x.replace(' a ','') for x in s]
            seq.append( (m.groups()[0], s))
            continue
        assert False, line

    floors = { 'first': 1, 'second': 2, 'third': 3, 'fourth': 4}
    elements = {}
    devices = { 'microchip': 'M', 'generator': 'G'}
    new_seq = []
    for (floor,lst) in seq:
        assert floor in floors
        new_lst = []
        for obj in lst:
            element, device = tuple(obj.split(' '))
            element = element.replace('-compatible','')
            if element not in elements:
                elements[element] = len(elements) 
            new_lst.append((elements[element],devices[device]))
        new_seq.append( (floors[floor],new_lst))

    return new_seq, elements

import itertools

def main(fp):
    seq, elements = parse(fp)
    print(seq,elements)
    entries = ['E']+list( itertools.product( list(range(len(elements))),'MG'))

    def check_elevator( elevator_objects):
        by_type = { 'G': [], 'M': []}
        assert len(elevator_objects) <= 2
        for i in elevator_objects:
            num, ty = entries[i]
            by_type[ty].append(num)
        if by_type['G'] and by_type['M']:
            return by_type['G'] == by_type['M']
        return True

    def check_floor( floor_objects):
        by_type = { 'G': [], 'M': []}
        for num, ty in floor_objects:
            by_type[ty].append(num)

        all_okay = True
        for m in by_type['M']:
            found_compatible = False
            found_incompatible = False
            for g in by_type['G']:
                if m == g:
                    found_compatible = True
                else:
                    found_incompatible = True
            if not found_compatible and found_incompatible:
                all_okay = False

        return all_okay

    def check_floors( state):
        by_floor = { 1: [], 2: [], 3: [], 4: []}
        for i in range(1,len(state)):
            by_floor[state[i]].append( entries[i])
        for i in range(1,5):
            if not check_floor( by_floor[i]):
                return False
        return True

    def gen_next_states( state):
        moves_from_state = []
        elevator_floor = state[0]
        objects_on_elevator_floor = [ idx for idx in range(1,len(state)) if state[idx] == elevator_floor]
        adjacent_floors = []
        if elevator_floor > 1:
            adjacent_floors.append(elevator_floor-1)
        if elevator_floor < 4:
            adjacent_floors.append(elevator_floor+1)

        for next_floor in adjacent_floors:
            for subset in itertools.chain(itertools.combinations(objects_on_elevator_floor,1),itertools.combinations(objects_on_elevator_floor,2)):
                lst_state = list(state)
                lst_state[0] = next_floor
                for idx in list(subset):
                    lst_state[idx] = next_floor
                next_state = tuple(lst_state)

                if check_elevator(subset) and check_floors(next_state):
                    yield next_state

    def get_init_state():
        init_state_lst = [None]*len(entries)
        init_state_lst[0] = 1
        for floor,lst in seq:
            for pair in lst:
                idx = entries.index(pair)
                print( pair, entries, idx)
                init_state_lst[idx] = floor

        return tuple(init_state_lst)

    def get_final_state():
        final_state_lst = [4]*len(entries)
        return tuple(final_state_lst)

    init_state = get_init_state()
    assert check_floors(init_state)
    final_state = get_final_state()

    path_length = 0
    valid_states = set()
    frontier_states = set()
    frontier_states.add(get_init_state())

    while True:
        valid_states = valid_states.union(frontier_states)
        new_frontier_states = set()
        for state in frontier_states:
            for next_state in gen_next_states(state):
                if next_state not in valid_states:
                    new_frontier_states.add(next_state)
        path_length += 1
        print( f'path_length: {path_length} new_frontier_states: {len(new_frontier_states)}')

        if final_state in new_frontier_states:
            return path_length
        frontier_states = new_frontier_states
            

@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 11 == main(fp)

@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

def test_C():
    with open('data_big', 'rt') as fp:
        print(main(fp))
