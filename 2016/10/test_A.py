import pytest
import io
import re
import hashlib

def v(o):
    if o is not None:
        return o.id()
    else:
        return None

class Bot:
    def __init__(self, num):
        self.num = num
        self.lo = None
        self.hi = None
        self.values = []
        
        self.incoming_edges = []

    def __repr__(self):
        return f"Bot(num={self.num},lo={v(self.lo)},hi={v(self.hi)},values={self.values},incoming_edges={self.incoming_edges})"
    def id(self):
        return f"Bot({self.num})"
    

class Output:
    def __init__(self, num):
        self.num = num
        self.values = []
    def __repr__(self):
        return f"Output(num={self.num},values={self.values})"
    def id(self):
        return f"Output({self.num})"

class Input:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Input(value={self.value})"
    def id(self):
        return f"Input({self.value})"


def parse(fp):
    bots = {}
    outputs = {}

    def get_or_add( tag, num):
        if tag == 'bot':
            if num not in bots:
                bots[num] = Bot(num)
            return bots[num]
        if tag == 'output':
            if num not in outputs:
                outputs[num] = Output(num)
            return outputs[num]
        assert False, tag
                
    seq = []
    p_bot = re.compile(r'^bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)$')
    p_value = re.compile(r'^value (\d+) goes to (output|bot) (\d+)$')

    for line in fp:
        line = line.rstrip('\n')
        m = p_bot.match(line)
        if m:
            bot = get_or_add( 'bot', int(m.groups()[0]))
            bot.lo = get_or_add( m.groups()[1], int(m.groups()[2]))
            bot.hi = get_or_add( m.groups()[3], int(m.groups()[4]))
            continue
        m = p_value.match(line)
        if m:
            obj = get_or_add( m.groups()[1], int(m.groups()[2]))
            obj.values.append( int(m.groups()[0]))
            continue
        assert False, line

    for (k,v) in bots.items():
        assert v.lo is not None
        assert v.hi is not None

    return bots, outputs

from collections import deque

def main(fp):
    bots, outputs = parse(fp)

    
    def build_incoming_edges(bots):
        for (k,v) in bots.items():
            v.incoming_edges = set()
        for (k,v) in bots.items():
            if type(v.lo) == Bot:
                v.lo.incoming_edges.add(v.num)
            if type(v.hi) == Bot:
                v.hi.incoming_edges.add(v.num)

    build_incoming_edges(bots)

    q = deque()

    for (k,v) in bots.items():
        if not v.incoming_edges:
            q.append(v)

    topo_order = []
    while q:
        c = q.popleft()
        topo_order.append(c)
        outgoing_edges = []
        if type(c.lo) == Bot:
            outgoing_edges.append(c.lo)
        if type(c.hi) == Bot:
            outgoing_edges.append(c.hi)
        for u in outgoing_edges:
            u.incoming_edges = u.incoming_edges.difference( set([c.num]))
            if not u.incoming_edges:
                q.append(u)
            
    print('topo_order:',[ x.num for x in topo_order])

    build_incoming_edges(bots)

    for v in topo_order:
        print(v)
        for u in list(v.incoming_edges):
            print('\t',bots[u])
            pass
        assert len(v.values) == 2, v
        v.lo.values.append(min(*v.values))
        v.hi.values.append(max(*v.values))
    for (k,out) in outputs.items():
        print(out)

    for v in topo_order:
        if set(v.values) == {61,17}:
            print('bot-61-17 is:', v.num)

    print('part2', outputs[0].values[0]*outputs[1].values[0]*outputs[2].values[0])
        


    return 0

def test_A():
    with open('data0', 'rt') as fp:
        assert 0 == main(fp)

#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        main(fp)
