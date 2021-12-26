from os import path
import re, io, pytest

from itertools import combinations, product
from collections import defaultdict, deque

def parse(fp):
    p2 = re.compile(r'^\s*(\S+)\s+(\S+)\s*$')
    p3 = re.compile(r'^\s*(\S+)\s+(\S+)\s+(\S+)\s*$')

    for line in fp:
        line = line.rstrip('\n')
        m = p2.match(line)
        if m:
            yield m.groups()
            continue

        m = p3.match(line)
        if m:
            yield m.groups()
            continue

        assert False, line

def legal_step(state, tape, cmd):
    state_dict = {k: v for k, v in zip("wxyz", state)}

    def get_possible_literal(c):
        if c in state_dict:
            return state_dict[c]
        else:
            return int(c)

    if cmd[0] == 'inp':
        if len(tape) == 0:
            return False
        else:
            return True
    else:
        a, b = state_dict[cmd[1]], get_possible_literal(cmd[2])
        if cmd[0] == 'add':
            return True
        elif cmd[0] == 'mul':
            return True
        elif cmd[0] == 'div':
            return b != 0
        elif cmd[0] == 'mod':
            return a >= 0 and b > 0
        elif cmd[0] == 'eql':
            return True
        else:
            return False

def step(state, tape, cmd):
    state_dict = {k: v for k, v in zip("wxyz", state)}

    def get_possible_literal(c):
        if c in state_dict:
            return state_dict[c]
        else:
            return int(c)

    if cmd[0] == 'inp':
        state_dict[cmd[1]] = tape.popleft()
    else:
        a, b = state_dict[cmd[1]], get_possible_literal(cmd[2])
        if cmd[0] == 'add':
            state_dict[cmd[1]] = a + b
        elif cmd[0] == 'mul':
            state_dict[cmd[1]] = a * b    
        elif cmd[0] == 'div':
            sa, sb = (1 if a >= 0 else -1), (1 if b >= 0 else -1)
            state_dict[cmd[1]] = sa * sb * ((a * sa) // (b * sb))
        elif cmd[0] == 'mod':
            state_dict[cmd[1]] = a % b
        elif cmd[0] == 'eql':
            state_dict[cmd[1]] = 1 if a == b else 0
        else:
            assert False, cmd

    return tuple(state_dict[c] for c in "wxyz"), tape

def test_add():
    assert step((0,1,2,3), deque([]), ('add', 'w', 'x')) == ((1,1,2,3), deque([]))

def test_inp():
    assert step((0,1,2,3), deque([1]), ('inp', 'w')) == ((1,1,2,3), deque([]))

def test_div():
    assert step((-5,2,0,0), deque([]), ('div', 'w', 'x')) == ((-2,2,0,0), deque([]))
    assert step((-5,-2,0,0), deque([]), ('div', 'w', 'x')) == ((2,-2,0,0), deque([]))
    assert step((5,2,0,0), deque([]), ('div', 'w', 'x')) == ((2,2,0,0), deque([]))
    assert step((5,-2,0,0), deque([]), ('div', 'w', 'x')) == ((-2,-2,0,0), deque([]))

def main(fp):
    cmds = list(parse(fp))
    groups = []
    for cmd in cmds:
        if cmd[0] == 'inp':
            groups.append([cmd])
        else:
            assert groups
            groups[-1].append(cmd)

    print([len(group) for group in groups])

    for i in range(len(groups[0])):
        cmds = [group[i] for group in groups]
        if all(cmds[0] == cmd for cmd in cmds):
            print(':'.join(cmds[0]))
        elif all(cmds[0][0] == cmd[0] and cmds[0][1] == cmd[1] for cmd in cmds):
            print(':'.join(cmds[0][:2]), [int(cmd[2]) for cmd in cmds])
        else:
            assert False

    ds = [int(group[4][2]) for group in groups]

    cs = [int(group[5][2]) for group in groups]
    es = [int(group[15][2]) for group in groups]

    print(ds, cs, es)



    states = { (0,0,0,0) : '' }

    for idx, group in enumerate(groups[:5]):
        new_states = {}
        for state0, path0 in states.items():
            for c in range(1,10):
                tape = deque([c])
                state = state0
                legal = True
                z = state[3]
                x = 1 if (z % 26 + cs[idx]) != c else 0
                z = (z // ds[idx])*(25*x+1)+x*(c+es[idx])
                for cmd in group:
                    if not legal_step(state, tape, cmd):
                        print('illegal step:', c, state, tape, cmd)
                        legal = False
                        break
                    state, tape = step(state, tape, cmd)
                assert not tape
                assert z == state[3]
                state = (0,0,0) + state[3:]
                cand = path0 + str(c)
                #print(state0, path0, c, legal, state, cand)
                if legal and (state not in new_states or cand > new_states[state]):
                    new_states[state] = cand


        states = new_states
        print(idx, len(states))

    return max( path for state,path in states.items() if state[3] == 0)



#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))
