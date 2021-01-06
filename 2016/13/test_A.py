import pytest
import io
import re

def main(*,secret_number,final):

    def pop_count( x):
        count = 0
        while x != 0:
            if x & 1 != 0:
                count += 1
            x >>= 1
        return count

    def is_open_space( state):
        (irow,icol) = state
        (y,x) = (irow,icol)
        return pop_count(x*x + 3*x + 2*x*y + y + y*y + secret_number) & 1 == 0

    def gen_next_states(state):
        adjacent_states = []
        (irow,icol) = state
        if irow > 0:
            adjacent_states.append( (irow-1,icol))
        if icol > 0:
            adjacent_states.append( (irow,icol-1))
        adjacent_states.append( (irow+1,icol))
        adjacent_states.append( (irow,icol+1))

        for next_state in adjacent_states:
            if is_open_space(next_state):
                yield next_state

    start = (1,1)

    print()
    for irow in range(10):
        print( ''.join( '.' if is_open_space( (irow,icol)) else '#' for icol in range(10)))

    valid_states = set()
    frontier_states = set()
    frontier_states.add(start)
    assert is_open_space(start)

    path_length = 0
    while frontier_states:
        valid_states = valid_states.union(frontier_states)
        new_frontier_states = set()
        for state in frontier_states:
            print(f'state: {state}')
            for next_state in gen_next_states(state):
                print(f'\tnext_state: {next_state}')
                if next_state not in valid_states:
                    new_frontier_states.add(next_state)
        path_length += 1
        print( f'path_length: {path_length} new_frontier_states: {len(new_frontier_states)}')

        if final in new_frontier_states:
            return path_length
        frontier_states = new_frontier_states

    return None

def main2(*,secret_number):

    def pop_count( x):
        count = 0
        while x != 0:
            if x & 1 != 0:
                count += 1
            x >>= 1
        return count

    def is_open_space( state):
        (irow,icol) = state
        (y,x) = (irow,icol)
        return pop_count(x*x + 3*x + 2*x*y + y + y*y + secret_number) & 1 == 0

    def gen_next_states(state):
        adjacent_states = []
        (irow,icol) = state
        if irow > 0:
            adjacent_states.append( (irow-1,icol))
        if icol > 0:
            adjacent_states.append( (irow,icol-1))
        adjacent_states.append( (irow+1,icol))
        adjacent_states.append( (irow,icol+1))

        for next_state in adjacent_states:
            if is_open_space(next_state):
                yield next_state

    start = (1,1)

    print()
    for irow in range(10):
        print( ''.join( '.' if is_open_space( (irow,icol)) else '#' for icol in range(10)))

    valid_states = set()
    frontier_states = set()
    frontier_states.add(start)
    assert is_open_space(start)

    path_length = 0
    while frontier_states and path_length < 50:
        valid_states = valid_states.union(frontier_states)
        new_frontier_states = set()
        for state in frontier_states:
            print(f'state: {state}')
            for next_state in gen_next_states(state):
                print(f'\tnext_state: {next_state}')
                if next_state not in valid_states:
                    new_frontier_states.add(next_state)
        path_length += 1
        print( f'path_length: {path_length} new_frontier_states: {len(new_frontier_states)}')
        frontier_states = new_frontier_states

    valid_states = valid_states.union(frontier_states)

    return len(valid_states)

def test_A():
    assert 11 == main(secret_number=10,final=(4,7))

    
"""
0123456789
##.######.
.0123##.#.
###.456###
#.####7###
......89##
#..##.#..#
###.#.....
..##.#####
.#.##....#
.##.#..#.#
"""

#@pytest.mark.skip
def test_B():
    print(main(secret_number=1350,final=(39,31)))
    print(main2(secret_number=1350))

