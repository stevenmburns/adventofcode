import pytest
import io
import re
import itertools
from collections import defaultdict

class Player:
    def __init__(self, id, p, c):
        self.id = id
        self.p = p
        self.c = c
        self.score = 0

    def __repr__(self):
        return str( (self.id,self.p,self.c,self.score))

class Board:
    def __init__(self,seq):
        self.board = [ list(line) for line in seq]

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

        self.positions = defaultdict(set)
        for player in self.players:
            self.positions[player.c].add( player.p)
        

    def is_empty(self, p, ignore_players=False):
        return self.board[p[0]][p[1]] == '.' and \
           ignore_players or p not in self.positions['G'] and p not in self.positions['E']

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
                    assert c == '.'
                    newline += 'G'
                elif p in self.positions['E']:
                    assert c == '.'
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

    def move_along_shortest_path(self,player):
        p,c = player.p,player.c
        opponent_type = 'G' if c == 'E' else 'E'

        targets = self.targets(opponent_type)
        opponents = self.current_player_positions(opponent_type)
        adjacent = set(self.gen_adjacent(p, ignore_players=True))

        print( p, adjacent, opponents)

        if adjacent.intersection(opponents):
            return

        found_targets = self.search(p, targets)

        if not found_targets:
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
            newp = min(first_steps)
            print( f'Moving player {player.id}, a {player.c}, from {player.p} to {newp}')
            self.positions[player.c].remove(player.p)
            player.p = newp
            self.positions[player.c].add(player.p)


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

    for _ in range(3):
        order = list(range(len(b.players)))
        order.sort( key=lambda idx: b.players[idx].p)
        for idx in order:
            player = b.players[idx]
            b.move_along_shortest_path(player)
        b.print_board()
    return 0

#@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 0 == main(fp)

@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))

@pytest.mark.skip
def test_AA():
    with open("data1","rt") as fp:
        assert (6,4) == main2(fp)

@pytest.mark.skip
def test_BB():
    with open("data","rt") as fp:
        print(main2(fp))
