import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def parse(fp):
    seq = []

    p0 = re.compile(r'^Immune System:$')
    p  = re.compile(r'^(\d+) units each with (\d+) hit points(.*) with an attack that does (\d+) (\S+) damage at initiative (\d+)\s*$')
    p1 = re.compile(r'^Infection:$')
    p2 = re.compile(r'^\s*$')

    pp = re.compile(r'(weak|immune) to (.*)$')

    state = None
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        if m:
            lst = m.groups()[2][2:-1].split('; ')
            l = []
            for s in lst:
                if s:
                    mm = pp.match(s)
                    assert mm, s
                    l.append( (mm.groups()[0], mm.groups()[1].split(', ')))

            seq.append( (state,int(m.groups()[0]),int(m.groups()[1]),l,int(m.groups()[3]),m.groups()[4],int(m.groups()[5])))
            continue
        m = p0.match(line)
        if m:
            state = 'Immune System'
            continue
        m = p1.match(line)
        if m:
            state = 'Infection'
            continue
        m = p2.match(line)
        if m:
            continue
        assert False, line
    return seq


class Group:
    @staticmethod
    def get_opposite( s):
        if s == 'Infection':
            return 'Immune System'
        elif s == 'Immune System':
            return 'Infection'
        else:
            assert False, s

    @property
    def effective_power(self):
        return self.units*self.damage

    def __init__(self, idx, id, tup):
        self.idx = idx
        self.id = id
        self.player = tup[0]
        self.opposite = self.get_opposite(self.player)
        self.units = tup[1]
        self.hit_points = tup[2]
        self.immunity = []
        self.weakness = []
        for (ty, lst) in tup[3]:
            if ty == 'immune':
                self.immunity.extend( lst)
            elif ty == 'weak':
                self.weakness.extend( lst)
            else:
                assert False, ty
        self.damage = tup[4]
        self.damage_type = tup[5]
        self.initiative = tup[6]

    def __repr__(self):
        return f"{self.player} ({self.opposite}) units={self.units} hit_points={self.hit_points} immunity={self.immunity} weakness={self.weakness} damage={self.damage} {self.damage_type} initiative={self.initiative}"

def target_selection( groups, player, debug=False):
    attackers = [ group for group in groups if group.player == player]
    attackers.sort( key=lambda p: (-p.effective_power, -p.initiative))

    defenders = [ group for group in groups if group.opposite == player]
    used_defenders = set()

    selections = []
    for attacker in attackers:
        if attacker.units == 0: continue
        selected_defender = None
        for defender in defenders:
            if defender.units == 0: continue
            if defender.idx in used_defenders: continue

            if attacker.damage_type in defender.immunity:
                #print( f'skipping {attacker} => {defender}')
                continue

            damage = attacker.effective_power
            if attacker.damage_type in defender.weakness:
                damage += attacker.effective_power

            if debug:
                print( f'{attacker.player} group {attacker.id+1} would deal defending group {defender.id+1} {damage} damage')

            metric = (damage, defender.effective_power, defender.initiative, defender.idx)
            if selected_defender is None or selected_defender < metric:
                selected_defender = metric

        if selected_defender is not None:
            used_defenders.add( selected_defender[3])

            if debug:
                print( f'considering {attacker.id+1} {attacker.player} {attacker.effective_power} => {selected_defender} {groups[selected_defender[3]].id+1}')
            
            selections.append( (attacker.idx, selected_defender[3]))

    return selections


def attack( groups, a, d, debug=False):
    attacker = groups[a]
    defender = groups[d]

    damage = attacker.effective_power
    if attacker.damage_type in defender.weakness:
        damage += attacker.effective_power

    total_points = defender.units * defender.hit_points
    total_points -= damage

    if total_points < 0:
        total_points = 0


    new_units = (total_points+defender.hit_points-1)//defender.hit_points

    if debug:
        print( f'{groups[a].player} group {groups[a].id+1} attacks defending group {groups[d].id+1}, killing {defender.units - new_units} units.')


    defender.units = new_units
    groups[d] = defender
    return groups

types = ['Immune System', 'Infection']

def print_groups(groups):
    print()
    for ty in types:
        print( f'{ty}:')
        for group in groups:
            if ty == group.player and group.units > 0:
                print( f'Group {group.id+1} contains {group.units} units')
                print( f'{group}')


def count_units(groups):
    sum = 0
    players_remaining = set()
    for group in groups:
        if group.units > 0:
            players_remaining.add(group.player)
            sum += group.units
    return sum, players_remaining

def run(groups):

    rounds = 0
    last_sum = None
    while True:
        if rounds % 1000 == 0:
            print( f'rounds {rounds}')
            #print_groups(groups)

        selections = []
        for ty in types:
            selections.extend( target_selection( groups, ty))

        selections.sort( key=lambda p: -groups[p[0]].initiative)

        if not selections:
            break

        #print( selections)
        for a,d in selections:
            groups = attack( groups, a, d)

        sum, winners = count_units(groups)

        if sum == last_sum:
            print( f'Stalemate {rounds}')
            return None, sum

        last_sum = sum

        rounds += 1


    assert len(winners) == 1

    return list(winners)[0], sum

def build_groups(seq,boost):
    groups = []

    ids = defaultdict(int)
    for idx,tup in enumerate(seq):
        groups.append( Group( idx, ids[tup[0]], tup))
        ids[tup[0]] += 1

    for group in groups:
        if group.player == 'Immune System':
            group.damage += boost

    return groups

def main(fp,boost=0):
    groups = build_groups(parse(fp),boost)
    return run(groups)

def main2(fp):
    seq = parse(fp)

    boost = 1
    
    lb = 0
    ub = None

    for _ in range(100):
        print(f'boost {boost}')
        winner, _ = run(build_groups(seq,boost))
        if winner == 'Immune System':
            ub = boost
            break
        else:
            lb = boost
        boost *= 2
        
    
    while True:
        print(f'lb {lb} ub {ub}')
        mid = (lb + ub)//2
        winner, count = run(build_groups(seq,mid))        
        if winner is not None or winner == 'Immune System':
            ub = mid
        else:
            lb = mid
        if lb >= ub - 1:
            break

    print(lb,ub)
    print( run(build_groups(seq,lb)))
    print( run(build_groups(seq,ub)))

    return 0


@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert ('Infection',5216) == main(fp)

@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert ('Immune System',51) == main(fp,1570)

@pytest.mark.skip
def test_A1():
    with open("data0","rt") as fp:
        assert ('Infection',139) == main(fp,1569)

#@pytest.mark.skip
def test_AA():
    with open("data0","rt") as fp:
        assert 0 == main2(fp)


@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))

