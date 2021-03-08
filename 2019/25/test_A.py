import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.DEBUG)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( [ int(x) for x in line.split(',')])

    assert len(seq) == 1

    return seq[0]

def gen_run(seq):
    pc = 0
    offset = 0

    seq_tbl = defaultdict(int)
    for idx,inst in enumerate(seq):
        seq_tbl[idx] = inst

    insts = { 1: lambda x,y: x+y,
              2: lambda x,y: x*y,
              7: lambda x,y: 1 if x < y else 0,
              8: lambda x,y: 1 if x == y else 0
    }

    jumps = { 5: lambda x: x != 0,
              6: lambda x: x == 0
    }

    def get_operand( mode, val):
        if mode == 0:
            return seq_tbl[val]
        elif mode == 1:
            return val
        elif mode == 2:
            return seq_tbl[val+offset]
        else:
            assert False, mode

    def set_value_to_operand( mode, val, value):
        if mode == 0:
            seq_tbl[val] = value
        elif mode == 1:
            assert False
        elif mode == 2:
            seq_tbl[val+offset] = value
        else:
            assert False, mode

    while True:
        cmd = seq_tbl[pc]
        op = cmd % 100


        cmd = cmd // 100
        modebits = [op]
        for _ in range(3):
            modebits.append(cmd % 10)
            cmd = cmd // 10

        if seq_tbl[pc] == 99:
            break

        if op == 3:
            set_value_to_operand( modebits[1], seq_tbl[pc+1], (yield))
            pc += 2
        elif op == 4:
            yield get_operand( modebits[1], seq_tbl[pc+1])
            pc += 2
        elif op == 9:
            offset += get_operand( modebits[1], seq_tbl[pc+1])
            pc += 2
        elif op in jumps:
            a = get_operand( modebits[1], seq_tbl[pc+1])
            b = get_operand( modebits[2], seq_tbl[pc+2])
            pc = b if jumps[op]( a) else pc+3
        elif op in insts:
            a = get_operand( modebits[1], seq_tbl[pc+1])
            b = get_operand( modebits[2], seq_tbl[pc+2])
            set_value_to_operand( modebits[3], seq_tbl[pc+3], insts[op]( a, b))
            pc += 4            
        else:
            assert False, modebits

def main(fp):
    insts = parse(fp)

    computer = gen_run(insts)

    def recv():
        s = ''
        while True:
            try:
                rc = next(computer)
                if rc is None:
                    break
                s += chr(rc)
            except StopIteration:
                break
        return s

    def send( s):
        result = []
        for c in s:
            rc = computer.send(ord(c))
            assert rc is None
        rc = computer.send(ord('\n'))
        return rc


    t = { 's': 'south', 'w': 'west', 'e': 'east', 'n': 'north'}

    if False:
        txt = 'wnne'
        print(recv())
        for c in txt:
            send(t[c])
            print(recv())

        while True:
            send(input())
            print(recv())

    def parse_take_response( s):
        p = re.compile( r'^You don\'t see that item here.$')
        p_weight_clue = re.compile( r'(heavier|lighter)')
        for line in s.split('\n'):
            m = p_weight_clue.match(line)
            if m:
                logging.error( f'Weight clue: {line}')
            m = p.match(line)
            if m:
                return False
        return True

    def parse_drop_response( s):
        p = re.compile( r'^You don\'t have that item.$')
        p_weight_clue = re.compile( r'(heavier|lighter)')
        for line in s.split('\n'):
            m = p_weight_clue.match(line)
            if m:
                logging.error( f'Weight clue: {line}')
            m = p.match(line)
            if m:
                return False
        return True


    def parse_response( s, print_line=False):
        p = re.compile( r'^== (.*) ==$')
        p_doors_header = re.compile( r'^Doors here lead:$')
        p_items_header = re.compile( r'^Items here:$')
        p_list_item = re.compile( r'^- (.*)$')

        p_weight_clue = re.compile( r'(heavier|lighter)')

        place = None
        doors = None
        items = None
        for line in s.split('\n'):
            m = p_weight_clue.match(line)
            if m:
                logging.error( f'Weight clue: {line}')

            m = p.match(line)
            if print_line:
                print(line)
            if m:
                place = m.groups()[0]
                continue
            m = p_doors_header.match(line)
            if m:
                doors = []
                continue
            m = p_items_header.match(line)
            if m:
                items = []
                continue
            m = p_list_item.match(line)
            if m:
                item = m.groups()[0]
                if items is not None:
                    items.append(item)
                else:
                    assert doors is not None
                    doors.append(item)

        return place, doors, items



    dirs = { 'north': (-1,0), 'east': (0, 1), 'south': (1,0), 'west': (0,-1)}
    opposite_door = { 'north': 'south', 'east': 'west', 'south': 'north', 'west': 'east'}
    dont_pick_up = { 'molten lava', 'photons', 'infinite loop'}

    def run_dfs():
        reached = {}
        path = []

        def dfs( u):
            place, doors, items = parse_response( recv())

            if u in reached:
                assert reached[u][0] == place
                return

            print( f'enter dfs({u}): {place} {doors}')

            reached[u] = (place, doors, items, path[:])

            for door in doors:
                print( f'\tchoose door {door}')
                d = dirs[door]
                v = u[0]+d[0], u[1]+d[1]
                assert 10 == send(door)
                path.append(door)
                dfs( v)
                path.pop()
                assert 10 == send(opposite_door[door])
                place1, doors1, items1 = parse_response( recv())
                assert place == place1 and doors == doors1

            print( f'leave dfs({u}): {place} {doors}')

        dfs( (0,0))
        assert not path
        return reached

    reached = run_dfs()

    for k, vv in reached.items():
        print(k)
        for v in vv:
            print( f'\t{v}')

    mrow,Mrow = None,None
    mcol,Mcol = None,None

    for (irow,icol),v in reached.items():
        if mrow is None or irow < mrow: mrow = irow
        if Mrow is None or irow > Mrow: Mrow = irow
        if mcol is None or icol < mcol: mcol = icol
        if Mcol is None or icol > Mcol: Mcol = icol

    print()
    for irow in range(mrow,Mrow+1):
        line = ''
        for icol in range(mcol,Mcol+1):
            line += '*' if (irow,icol) == (0,0) else '#' if (irow,icol) in reached else '.'
        print(line)

    all_items = set()
    for k,v in reached.items():
        place, doors, items, path = v
        if items is None: items = []
        for item in items:
            all_items.add(item)

    okay_items = list(all_items.difference(dont_pick_up))

    print(len(okay_items), okay_items)

    power_set = list()
    for i in range( 1<<len(okay_items)):
        s = []
        for j in range(len(okay_items)):
            if i & (1<<j) != 0:
                s.append(j)
        power_set.append( frozenset(s))

    items_to_state = {}
    for k, v in reached.items():
        _, _, items, _ = v
        if items is not None:
            if items:
                assert len(items) == 1
                items_to_state[items[0]] = k

    print(items_to_state)

    print(power_set)

    def get_items_in_set(s):
        for i in s:
            item = okay_items[i]
            p = items_to_state[item]

            place, doors, items, path = reached[p]
            
            assert item == items[0]

            logging.debug( f'path to {p} {path}')
            for door in path:
                assert 10 == send(door)                
                place1, doors1, items1 = parse_response( recv())
                logging.debug( f'\t{place1} {items1}')

            logging.debug( f'trying to take {item}')
            send(f'take {item}')
            assert parse_take_response(recv())

            for door in reversed(path):
                assert 10 == send(opposite_door[door])                
                place1, doors1, items1 = parse_response( recv())

    def get_all_items():
        get_items_in_set( set(range(len(okay_items))))

    def return_items_in_set(s):
        for i in s:
            item = okay_items[i]
            p = items_to_state[item]

            place, doors, items, path = reached[p]
            
            assert item == items[0]

            logging.debug( f'path to {p} {path}')
            for door in path:
                assert 10 == send(door)                
                place1, doors1, items1 = parse_response( recv())
                logging.debug( f'\t{place1} {items1}')

            logging.debug( f'trying to drop {item}')
            send(f'drop {item}')
            assert parse_drop_response(recv())

            for door in reversed(path):
                assert 10 == send(opposite_door[door])                
                place1, doors1, items1 = parse_response( recv())

    def return_all_items():
        return_items_in_set( set(range(len(okay_items))))

    
    if False:
        get_all_items()

        for p, (place,doors,items,path) in reached.items():

            print(f'Working on {p}')

            for door in path:
                assert 10 == send(door)                
                place1, doors1, items1 = parse_response( recv())
                print( f'{place1}')

            for s in power_set:
                print(f'\tWorking on {s}')

                for i in s:
                    item = okay_items[i]
                    send(f'drop {item}')
                    assert parse_drop_response(recv()), (i,s)

                if path:
                    for door in doors1:
                        assert 10 == send(door)                
                        _ = parse_response( recv(), print_line=True)
                        assert 10 == send(opposite_door[door])                
                        _ = parse_response( recv(), print_line=True)

                for i in s:
                    item = okay_items[i]
                    send(f'take {item}')
                    assert parse_take_response(recv()), (i,s)

            for door in reversed(path):
                assert 10 == send(opposite_door[door])                
                place1, doors1, items1 = parse_response( recv())


        return_all_items()

    if False:
        for s in power_set:
            print( s)
            get_items_in_set(s)

            if True:
                send('south')
                _, _, _ = parse_response( recv())
                send('north')
                reached1 = run_dfs()
                logging.info( f'{okay_items}')

                places = set( p[0] for p in reached.values())
                places1 = set( p[0] for p in reached1.values())
                logging.info( f'{set(s)} {places} {places1}')
                assert places == places1

                if True:
                    send('inv')
                    txt = recv()
                    logging.info(txt)

            return_items_in_set(s)


    return 0

    """
.#.
##.
##.
##.
#*.
###
"""



#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))
