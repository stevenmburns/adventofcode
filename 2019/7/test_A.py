import pytest
import io
import re
import itertools
from collections import defaultdict, deque
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append( [ int(x) for x in line.split(',')])

    assert len(seq) == 1

    return seq[0]

def run(seq,inps):
    pc = 0

    insts = { 1: lambda x,y: x+y,
              2: lambda x,y: x*y,
              7: lambda x,y: 1 if x < y else 0,
              8: lambda x,y: 1 if x == y else 0
    }

    outs = []

    def get_operand( mode, val):
        if mode == 0:
            return seq[val]
        else:
            return val

    while True:

        if seq[pc] == 99:
            break

        cmd = seq[pc]
        op = cmd % 100
        cmd = cmd // 100
        modebits = [op]
        for _ in range(2):
            modebits.append(cmd % 10)
            cmd = cmd // 10

        logging.info( f'{pc} {modebits} {seq[pc:pc+8]}')

        if op == 3:
            assert modebits[1] == 0
            seq[seq[pc+1]] = inps.popleft()
            pc += 2
        elif op == 4:
            outs.append( get_operand( modebits[1], seq[pc+1]))
            pc += 2
        elif op == 5:
            if get_operand( modebits[1], seq[pc+1]) != 0:
                pc = get_operand( modebits[2], seq[pc+2])
            else:
                pc += 3
        elif op == 6:
            if get_operand( modebits[1], seq[pc+1]) == 0:
                pc = get_operand( modebits[2], seq[pc+2])
            else:
                pc += 3
        elif op in insts:
            a = get_operand( modebits[1], seq[pc+1])
            b = get_operand( modebits[2], seq[pc+2])
            c = seq[pc+3]
            seq[c] = insts[op]( a, b)
            pc += 4            
        else:
            assert False, modebits

    return outs

def gen_run(seq):
    pc = 0

    insts = { 1: lambda x,y: x+y,
              2: lambda x,y: x*y,
              7: lambda x,y: 1 if x < y else 0,
              8: lambda x,y: 1 if x == y else 0
    }

    outs = []

    def get_operand( mode, val):
        if mode == 0:
            return seq[val]
        else:
            return val

    while True:

        if seq[pc] == 99:
            break

        cmd = seq[pc]
        op = cmd % 100
        cmd = cmd // 100
        modebits = [op]
        for _ in range(2):
            modebits.append(cmd % 10)
            cmd = cmd // 10

        logging.info( f'{pc} {modebits} {seq[pc:pc+8]}')

        if op == 3:
            assert modebits[1] == 0
            seq[seq[pc+1]] = (yield)
            pc += 2
        elif op == 4:
            yield get_operand( modebits[1], seq[pc+1])
            pc += 2
        elif op == 5:
            if get_operand( modebits[1], seq[pc+1]) != 0:
                pc = get_operand( modebits[2], seq[pc+2])
            else:
                pc += 3
        elif op == 6:
            if get_operand( modebits[1], seq[pc+1]) == 0:
                pc = get_operand( modebits[2], seq[pc+2])
            else:
                pc += 3
        elif op in insts:
            a = get_operand( modebits[1], seq[pc+1])
            b = get_operand( modebits[2], seq[pc+2])
            c = seq[pc+3]
            seq[c] = insts[op]( a, b)
            pc += 4            
        else:
            assert False, modebits

    return outs

def main(fp):
    seq = parse(fp)

    results = []

    for phase_settings in itertools.permutations(range(5)):
        inps = deque()
        inps.append(0)
        
        for phase_setting in phase_settings:
            inps.appendleft(phase_setting)
            outs = run(seq[:],inps)
            assert len(outs) == 1
            assert len(inps) == 0
            inps.append(outs.pop())
        
        results.append( (inps[0], phase_settings))

    results.sort()

    print(results)
        
    return results[-1][0]

def main2(fp):
    seq = parse(fp)

    results = []

    for phase_settings in itertools.permutations(range(5,10)):
        stages = [ gen_run(seq[:]) for _ in range(5)]

        for idx, phase_setting in enumerate(phase_settings):
            next(stages[idx])
            stages[idx].send(phase_setting)

        v = 0
        done = False
        ampe = None

        first = True

        while not done:
            for stage in stages:
                if not first:
                    try:
                        next(stage)
                    except StopIteration:
                        done = True
                        break

                v = stage.send(v)
            first = False
            ampe = v
            print( f'ampe {ampe}')

        for stage in stages:
            stage.close()

        results.append( (ampe, phase_settings))

    results.sort()

    print(results)
        
    return results[-1][0]

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))


