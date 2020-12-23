
import io

import logging
from logging import debug
import re

#logging.basicConfig(level=logging.DEBUG)

def main( fp):
    #debug("Part 1")

    groups = []
    group = []
    for line in fp:
        line = line.rstrip('\n')
        if line == '':
            groups.append(group)
            group = []
        else:
            group.append(line)
    groups.append(group)    

    sum = 0
    for group in groups:
        q = set()
        for s in group:
            for c in s:
                q.add(c)
        sum += len(q)

    print(groups)
    return sum

def main2( fp):
    #debug("Part 1")

    groups = []
    group = []
    for line in fp:
        line = line.rstrip('\n')
        if line == '':
            groups.append(group)
            group = []
        else:
            group.append(line)
    groups.append(group)    

    sum = 0
    for group in groups:
        qq = None
        for s in group:
            q = set()
            for c in s:
                q.add(c)
            if qq is None:
                qq = q
            else:
                qq = qq.intersection(q)
        sum += len(qq)

    print(groups)
    return sum

def test_A():
    fp = io.StringIO( """abc

a
b
c

ab
ac

a
a
a
a

b
""")

    #assert 11 == main(fp)
    assert 6 == main2(fp)

def test_B():
    with open( "data", "rt") as fp:
        #print(main(fp))
        print(main2(fp))
    
