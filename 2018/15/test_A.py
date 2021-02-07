import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)

class Player:
    def __init__(self, id, p, c):
        self.id = id
        self.p = p
        self.c = c
        self.hit_points = 200

    def __repr__(self):
        return str( (self.id,self.p,self.c,self.hit_points))

class Board:
    def __init__(self,seq,elf_attack_power=3):
        self.board = [ list(line) for line in seq]

        self.elf_attack_power = elf_attack_power
        self.players = []
        self.board = []
        for irow,line in enumerate(seq):
            newline = ''
            for icol,c in enumerate(line):
                if c in 'GE':
                    self.players.append( Player( len(self.players), (irow,icol),c))
                    newline += '.'
                else:
                    newline += c
            self.board.append(newline)

        self.position_map = {}
        self.positions = defaultdict(set)
        for player in self.players:
            self.position_map[player.p] = player.id
            self.positions[player.c].add( player.p)

    def is_empty(self, p, ignore_players=False):
        return self.board[p[0]][p[1]] == '.' and \
           (ignore_players or p not in self.positions['G'] and p not in self.positions['E'])

    @property
    def nrows(self):
        return len(self.board)

    @property
    def ncols(self):
        return len(self.board[0])

    def print_board(self):
        print()
        for irow,line in enumerate(self.board):
            newline = ''
            for icol,c in enumerate(line):
                p = irow,icol
                if p in self.positions['G']:
                    assert c == '.', p
                    newline += 'G'
                elif p in self.positions['E']:
                    assert c == '.', p
                    newline += 'E'
                else:
                    newline += c
            print(''.join(newline))

    def current_player_positions(self,ty):
        return self.positions[ty]

    def gen_adjacent(self, p, ignore_players=False):
        irow,icol = p
        for drow,dcol in [(0,-1),(0,1),(-1,0),(1,0)]:
            jrow,jcol = irow+drow,icol+dcol
            if 0 <= jrow < self.nrows and 0 <= jcol < self.ncols:
                if self.is_empty( (jrow,jcol), ignore_players):
                    yield (jrow,jcol)

    def targets(self,opponent):
        s = set()
        for p in self.current_player_positions(opponent):
            for jp in self.gen_adjacent(p):
                s.add( jp)
        return s

    def search(self, p, targets):
        reached = set()
        frontier = { p }

        steps = 0
        while frontier:

            found_targets = targets.intersection(frontier)
            if found_targets:
                break

            new_frontier = set()
            for irow,icol in frontier:
                for p in self.gen_adjacent( (irow,icol)):
                    new_frontier.add( p)

            reached = reached.union(frontier)
            frontier = new_frontier.difference(reached)

            steps += 1

        #print( f'found path of length {steps} from {p} to {found_targets}')

        return found_targets

    def attack(self,player):
        p,c = player.p,player.c
        opponent_type = 'G' if c == 'E' else 'E'

        targets = self.targets(opponent_type)
        opponents = self.current_player_positions(opponent_type)
        adjacent = set(self.gen_adjacent(p, ignore_players=True))

        potential_victims = adjacent.intersection(opponents)

        if potential_victims:
            def k(p):
                idx = self.position_map[p]
                victim = self.players[idx]
                assert victim.p == p
                return victim.hit_points,p
            victim = self.players[self.position_map[min( potential_victims, key=k)]]
            logging.debug( f'Player {player} attacking {victim}')
            victim.hit_points -= self.elf_attack_power if player.c == 'E' else 3
            if victim.hit_points <= 0:
                logging.debug( f'Remove victim {victim}')
                del self.position_map[victim.p]
                self.positions[victim.c].remove(victim.p)

    def move_and_update(self, player, newp):
        logging.debug( f'Moving player {player.id}, a {player.c}, from {player.p} to {newp}')
        del self.position_map[player.p]
        self.positions[player.c].remove(player.p)
        player.p = newp
        self.position_map[player.p] = player.id
        self.positions[player.c].add(player.p)


    def move_along_shortest_path(self,player):
        p,c = player.p,player.c
        opponent_type = 'G' if c == 'E' else 'E'

        targets = self.targets(opponent_type)
        opponents = self.current_player_positions(opponent_type)
        adjacent = set(self.gen_adjacent(p, ignore_players=True))

        if adjacent.intersection(opponents):
            logging.debug(f"Player {player} can attack. No move")
            return

        if not targets:
            logging.debug(f"No targets for player {player}")
            return

        found_targets = self.search(p, targets)

        if not found_targets:
            logging.debug(f"No reachable targets for player {player}")
            return

        selected_target = min(found_targets)

        reached = set()
        frontier = { selected_target }

        targets = set()
        irow,icol = p
        for jp in self.gen_adjacent( p):
            targets.add( jp)

        first_steps = self.search( selected_target, targets)

        if first_steps:
            self.move_and_update( player, min(first_steps))


def parse(fp):
    seq = []
    for line in fp:
        line = line.rstrip('\n')
        seq.append(line)
    return seq

def main(fp):
    seq = parse(fp)
    b = Board(seq)

    b.print_board()
    print(b.players)

    for rounds in range(0,10000):
        order = list(range(len(b.players)))
        order.sort( key=lambda idx: b.players[idx].p)
        for idx in order:
            player = b.players[idx]
            if player.hit_points <= 0: continue
            b.move_along_shortest_path(player)
            b.attack(player)
        b.print_board()
        if not b.positions['G'] or not b.positions['E']:
            break

    sum = 0
    for player in b.players:
        if player.hit_points > 0:
            sum += player.hit_points

    print(sum,rounds)

    return { sum * rounds, sum * (rounds+1)}

def aux(seq,elf_attack_power):

    b = Board(seq,elf_attack_power)

    starting_num_of_elves = len(b.positions['E'])

    #b.print_board()
    #print(b.players)


    for rounds in range(0,10000):
        order = list(range(len(b.players)))
        order.sort( key=lambda idx: b.players[idx].p)
        for idx in order:
            player = b.players[idx]
            if player.hit_points <= 0: continue
            b.move_along_shortest_path(player)
            b.attack(player)
        #b.print_board()
        if not b.positions['G'] or not b.positions['E']:
            break

    sum = 0
    for player in b.players:
        if player.hit_points > 0:
            sum += player.hit_points

    print(sum,rounds, sum*rounds, sum*(rounds+1))

    return len(b.positions['E']) == starting_num_of_elves

def main2(fp):
    seq = parse(fp)
    for elf_attack_power in range(3,100):
        logging.info(f'Trying with elf_attack_power {elf_attack_power}')
        if aux(seq,elf_attack_power):
            return elf_attack_power
    return None

@pytest.mark.skip
def test_A0():
    with open("data0","rt") as fp:
        assert 0 == main(fp)

@pytest.mark.skip
def test_A1():
    with open("data1","rt") as fp:
        assert 27730 in main(fp)

@pytest.mark.skip
def test_A2():
    with open("data2","rt") as fp:
        assert 36334 in main(fp)

@pytest.mark.skip
def test_A3():
    with open("data3","rt") as fp:
        assert 39514 in main(fp)


@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))

