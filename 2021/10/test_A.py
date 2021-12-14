from functools import reduce

def parse(fp):
    for line in fp:
        yield line.rstrip('\n')

m = { '{':'}', '[':']', '(':')', '<':'>' }

def aux(line):
    stack = []
    im = { v: k for k, v in m.items() }
    for c in line:
        if c in m:
            stack.append(c)
        elif c in im:
            if not stack or im[c] != stack[-1]:
                return c, stack
            stack.pop()
    else:
        return None, stack

def main(fp):
    tbl = { ')' : 3, '}' : 1197, ']' : 57, '>' : 25137 }
    return sum(tbl[p[0]] if (p := aux(line))[0] is not None else 0
                for line in parse(fp))

def main2(fp):
    tbl = { ')' : 1, '}' : 3, ']' : 2, '>' : 4 }
    scores = list(sorted(reduce(lambda x, y: x*5 + tbl[m[y]], reversed(p[1]), 0) 
                    for line in parse(fp) if (p := aux(line))[0] is None))
    return scores[len(scores)//2]

def test_A0():
    with open('data0') as fp:
        assert 26397 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA0():
    with open('data0') as fp:
        assert 288957 == main2(fp)

def test_BB():
    with open('data') as fp:
        print(main2(fp))
