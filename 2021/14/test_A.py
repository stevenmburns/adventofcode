from functools import reduce
import pytest, re
from collections import Counter

def parse(fp):
    p_rule = re.compile(r'^(\S\S) \-> (\S)$')
    p_blank = re.compile(r'^\s*$')
    p_s = re.compile(r'^(\S+)$')

    s = None

    rules = []

    for line in fp:
        line = line.rstrip('\n')
        m = p_s.match(line)
        if m:
            s = m.groups()[0]
            continue
        m = p_blank.match(line)
        if m:
            continue
        m = p_rule.match(line)
        if m:
            rules.append((m.groups()[0], m.groups()[1]))
            continue

    return s, dict(rules)

def step(s, rules):

    r = [s[0]]

    for i in range(1, len(s)):
        if s[i-1:i+1] in rules:
            r.append(rules[s[i-1:i+1]])
        r.append(s[i])

    return ''.join(r)



def main(fp):
    s, rules = list(parse(fp))

    for _ in range(10):
        s = step(s, rules)
        #print(s)

    histo = Counter(s)
    m, M = min(histo.values()), max(histo.values())
    return M - m

def step2(h, rules):

    r = Counter()

    for pair, count in h.items():
        if pair in rules:
            new = rules[pair]
            left = pair[0] + new
            right = new + pair[1]
            r[left] += count
            r[right] += count

    return r

def main2(fp, n=40):
    s, rules = list(parse(fp))

    pairs = [a+b for a,b in zip(s, s[1:])]

    h = Counter(pairs)

    #print(h)

    for _ in range(n):
        h = step2(h, rules)
        #print(h)

    histo = Counter()

    for pair, count in h.items():
        histo[pair[0]] += count
        histo[pair[1]] += count

    histo[s[0]] += 1
    histo[s[-1]] += 1

    assert all(v % 2 == 0 for v in histo.values())

    m, M = min(histo.values()), max(histo.values())
    return (M - m) // 2

#@pytest.mark.skip
def test_A0():
    with open('data0') as fp:
        assert 1588 == main(fp)

#@pytest.mark.skip
def test_B():
    with open('data') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_AAA0():
    with open('data0') as fp:
        assert 1588 == main2(fp, n=10)

#@pytest.mark.skip
def test_AA0():
    with open('data0') as fp:
        assert 2188189693529 == main2(fp)

#@pytest.mark.skip
def test_BB():
    with open('data') as fp:
        print(main2(fp))
