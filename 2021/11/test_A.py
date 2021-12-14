from functools import reduce

def parse(fp):
    for line in fp:
        yield [int(x) for x in line.rstrip('\n')]

def step(data):
    m = len(data)
    n = len(data[0])

    def adjacent(u):
        i, j = u
        for di in range(-1,2):
            for dj in range(-1,2):
                if di == 0 and dj == 0:
                    continue
                if 0 <= i+di < m and 0 <= j+dj < n:
                    yield (i+di, j+dj)

    for i in range(m):
        for j in range(n):
            data[i][j] += 1

    frontier = set()
    for i in range(m):
        for j in range(n):
            if data[i][j] > 9:
                frontier.add((i,j))

    flash = set()

    while frontier:
        newfrontier = set()
        for i,j in frontier:
            for ii, jj in adjacent((i,j)):
                data[ii][jj] += 1
                if data[ii][jj] > 9:
                    newfrontier.add((ii,jj))
        flash.update(frontier)
        frontier = newfrontier.difference(flash)

    for i, j in flash:  
        data[i][j] = 0

    return data, len(flash)

def print_board(data):
    print("----------------")
    for row in data:
        print(''.join(str(x) for x in row))


def main(fp):
    data = list(parse(fp))
    s = 0
    print_board(data)
    for _ in range(100):
        data, number_of_flashes = step(data)
        print_board(data)
        s += number_of_flashes

    return s

def main2(fp):
    data = list(parse(fp))
    m = len(data)
    n = len(data[0])


    #print_board(data)
    i = 0
    while True:
        data, number_of_flashes = step(data)
        #print_board(data)
        i += 1
        if number_of_flashes == m*n:
            return i

def test_A1():
    with open('data1') as fp:
        main(fp)

def test_A0():
    with open('data0') as fp:
        assert 1656 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA0():
    with open('data0') as fp:
        assert 195 == main2(fp)

def test_BB():
    with open('data') as fp:
        print(main2(fp))
