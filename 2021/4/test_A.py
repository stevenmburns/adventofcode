import re
from itertools import product

def parse(fp):
    p = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$')
    order = None
    boards = []
    board = None
    for line in fp:
        line = line.rstrip('\n')
        if order is None:
            order = [int(x) for x in line.split(',')]
        elif line == '':
            board = []
        else:
            m = p.match(line)
            assert m is not None
            board.append([int(x) for x in m.groups()])
            if len(board) == 5:
                boards.append(board)
                board = None

    assert board is None

    return boards, order

class Board:
    def __init__(self, board):
        self.board = board
        self.m = {v : (i,j) for i, row in enumerate(board) for j, v in enumerate(row)}
        self.occupied = set()

    def is_winner(self):
        for i in range(5):
            if all( (i,j) in self.occupied for j in range(5) ):
                return True

        for j in range(5):
            if all( (i,j) in self.occupied for i in range(5) ):
                return True

        return False

    def score(self):
        if not self.is_winner():
            return 0
    
        return sum(self.board[i][j] for i, j in product(range(5),range(5)) if (i,j) not in self.occupied)
        




def main(fp):
    boards, order = parse(fp)

    boards = [Board(board) for board in boards]


    for idx, i in enumerate(order):
        for board in boards:
            if i in board.m:
                board.occupied.add( board.m[i] )

        winners = [ b for b, board in enumerate(boards) if board.is_winner()]
        if winners:
            return boards[winners[0]].score()*i

def main2(fp):
    boards, order = parse(fp)

    boards = [Board(board) for board in boards]

    already_won = set()
    winning_order = []

    for i in order:
        for b, board in enumerate(boards):
            if i in board.m:
                board.occupied.add( board.m[i] )
            if board.is_winner() and b not in already_won:
                winning_order.append( (b, board.score()*i))
                already_won.add(b)

    return winning_order[-1][1]    


def test_A0():
    with open('data0') as fp:
        assert 4512 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA0():
    with open('data0') as fp:
        assert 1924 == main2(fp)

def test_BB():
    with open('data') as fp:
        print(main2(fp))