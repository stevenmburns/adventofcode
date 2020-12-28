import io
import pytest

class Leaf:
    def __init__(self,c):
        self.c = c
    def __repr__(self):
        return self.c

def parse(fp):
    messages_now = False
    messages = []

    tbl = {}
    for line in fp:
        line = line.rstrip('\n')
        state = None
        expr = []
        term = []
        for token in line.split(" "):
            if messages_now:
                if len(token) == 0:
                    pass
                else:
                    messages.append(token)
            else:
                if len(token) == 0:
                    messages_now = True
                elif token[-1] == ':':
                    state = int(token[:-1])
                elif token == '|':
                    expr.append(term)
                    term = []
                elif token[0] == '"':
                    term.append(Leaf(token[1]))
                else:
                    term.append(int(token))
        if not messages_now:
            expr.append(term)
            tbl[state] = expr
    return tbl, messages

def isvalid( tbl, message):
    
    def gen0( rule, cursor):
        if type(rule) == Leaf:
            if cursor < len(message) and message[cursor] == rule.c:
                yield cursor+1
        else:
            yield from gen2( tbl[rule], cursor)

    def gen1( lst, cursor):
        if len(lst) == 1:
            yield from gen0( lst[0], cursor)
        else:
            for next_cursor in gen0( lst[0], cursor):
                yield from gen1( lst[1:], next_cursor)

    def gen2( lol, cursor):
        for lst in lol:
            yield from gen1(lst, cursor)

    for next_cursor in gen0( 0, 0):
        if next_cursor == len(message):
            return True

    return False


def main(fp):
    tbl, messages = parse(fp)

    count = 0
    for message in messages:
        if isvalid( tbl, message):
            count += 1

    print(f"count: {count}")
    return count
    
def test_A():
    txt = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

    with io.StringIO(txt) as fp:
        assert main(fp) == 2

def test_AA():
    txt = """0: 4 5 | 4 0 5
4: "a"
5: "b"

a
b
ab
aabb
aaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbb
aabbb
"""
    with io.StringIO(txt) as fp:
        assert main(fp) == 3

def test_AAA():
    txt = """0: 2
2: "a" 2 "a" | "a" "a"

aaaa
aa
aaa
a
"""
    with io.StringIO(txt) as fp:
        assert main(fp) == 2

def test_AAAA():
    txt = """0: 1
1: "b" 1 | "b"

bb
bbb
"""
    with io.StringIO(txt) as fp:
        assert main(fp) == 2

def test_AAAAA():
    txt = """0: "b" | "b" 0

bbb
"""
    with io.StringIO(txt) as fp:
        assert main(fp) == 1

def test_B():
    txt = """0: 1 2
1: "a"
2: "b"

ab
aba
ba
a
b
"""
    with io.StringIO(txt) as fp:
        assert main(fp) == 1

def test_C():
    with open( "data", "rt") as fp:
        main(fp)

def test_D():
    with open( "data1", "rt") as fp:
        main(fp)
