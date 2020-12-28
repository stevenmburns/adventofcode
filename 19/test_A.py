import io
import pytest

class Leaf:
    def __init__(self,c):
        self.c = c
    def __repr__(self):
        return self.c

from logging import debug
import logging

logging.basicConfig(level=logging.DEBUG)

def isvalid( tbl, state, seq):

    debug("="*80)
    debug(f"isvalid: {state} {seq}")

    def aux( lst_of_lst, *, level):
        nonlocal cursor
        debug( f"{' '*(3*level)}aux: lol: {lst_of_lst} cursor: {cursor} remaining: {seq[cursor:]}")
        save_cursor = cursor
        for terms in lst_of_lst:
            debug(f"{' '*(3*level)}setting cursor to {save_cursor}")
            cursor = save_cursor
            failed = False
            for term in terms:
                if failed: continue
                debug( f"{' '*(3*level)}term {term} cursor {cursor} remaining {seq[cursor:]}")
                if type(term) == Leaf:
                    debug( f"{' '*(3*level)}Leaf seq {seq} cursor {cursor} term.c {term.c}")
                    if cursor < len(seq) and term.c == seq[cursor]:
                        debug( f"{' '*(3*level)}Match")
                        cursor += 1
                    else:
                        debug( f"{' '*(3*level)}No Match")
                        failed = True
                else:
                    debug( f"{' '*(3*level)}non-Leaf: term {term} cursor {cursor} remaining {seq[cursor:]}")
                    if not aux( tbl[term], level=level+1):
                        failed = True
                debug( f"{' '*(3*level)}end of terms loop: cursor {cursor} remaining {seq[cursor:]}")

            debug( f"{' '*(3*level)}end of lol loop: failed {failed} level {level} cursor {cursor}")
            if not failed and level > 0:
                return True
            if not failed and level == 0 and cursor == len(seq):
                debug( f"{' '*(3*level)}Found")
                return True

        return False

    cursor = 0
    return aux( tbl[state], level=0)

def main(fp):

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
    debug(tbl,messages)

    count = 0
    for message in messages:
        if isvalid( tbl, 0, message):
            count += 1

    print(f"count: {count}")
    return count
    
@pytest.mark.skip
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

@pytest.mark.skip
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

@pytest.mark.skip
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

@pytest.mark.skip
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

@pytest.mark.skip
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

@pytest.mark.skip
def test_C():
    with open( "data", "rt") as fp:
        main(fp)

@pytest.mark.skip
def test_D():
    with open( "data1", "rt") as fp:
        main(fp)
