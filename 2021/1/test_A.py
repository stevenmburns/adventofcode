
import io

def parse(fp):
    for line in fp:
        line = line.rstrip('\n')
        yield int(line)

def main(fp):
    lst = list(parse(fp))
    return sum( 1 for a,b in zip(lst, lst[1:]) if a<b )


def main2(fp):
    lst = list(parse(fp))
    lst0 = [a+b+c for a,b,c in zip(lst, lst[1:], lst[2:])]
    return sum( 1 for a,b in zip(lst0, lst0[1:]) if a<b )


def test_A0():
    txt = """199
200
208
210
200
207
240
269
260
263
"""

    assert 7 == main(io.StringIO(txt))


def test_B():
    with open('data') as fp:
        print(main(fp))


def test_BB():
    with open('data') as fp:
        print(main2(fp))
    