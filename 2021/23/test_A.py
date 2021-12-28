
from copy import deepcopy
from collections import defaultdict
import heapq

def parse(txt):
    grid = txt.split('\n')[:-1]
    n = len(grid[0])
    for i in range(len(grid)):
        grid[i] = list(grid[i] + ' ' * (n - len(grid[i])))

    return grid

def prnt(grid):
    for row in grid:
        print(''.join(row))

def state_to_grid(state, nodes, template):
    grid = deepcopy(template)
    for (i, j), c in zip(nodes, state):
        grid[i][j] = c
    return grid

def grid_to_state(nodes, grid):
    state = []
    for i, j in nodes:
        state.append(grid[i][j])

    return tuple(state)




def main(txt):
    grid = parse(txt)
    m = len(grid)
    n = len(grid[0])

    nodes = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in '.ABCD':
                nodes.append((i, j))
                
    inv_nodes = { k: idx for idx, k in enumerate(nodes) }

    costs = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }

    def move( i, j, ii, jj, grid):
        assert grid[i][j] not in ' #.'
        assert grid[ii][jj] == '.'
        assert not ( ii == 1 and jj in [3,5,7,9] )
        token = grid[i][j]
        grid[ii][jj] = token
        grid[i][j] = '.'

        #prnt(grid)

        if i > 1 and ii > 1:
            dist = i-1 + ii-1 + abs(j-jj)
        else:
            dist = abs(i-ii)+abs(j-jj)

        cost = dist * costs[token]

        #print( f'----{cost}----')

        return cost

    def potential_moves(grid):
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] in 'ABCD':
                    for ii in range(m):
                        for jj in range(n):
                            if grid[ii][jj] == '.':
                                yield (i, j, ii, jj)

    columns = { 'A': 3, 'B': 5, 'C': 7, 'D': 9 }
    inv_columns = { v: k for k, v in columns.items() }

    def legal_move( move, grid):
        m = len(grid)
        i, j, ii, jj = move
        token = grid[i][j]

        # illegal landing spot
        if jj in inv_columns:
            if jj != columns[token]:
                return False

            if ii == 1:
                return False

            for iii in range(ii+1, m-1):
                if grid[iii][jj] != token:
                    return False

        if i == 1 and ii == 1: # I-route
            return False



        elif i == 1 and ii > 1: # L-route
            if j < jj:
                for jjj in range(j+1, jj+1):
                    if grid[i][jjj] != '.':
                        return False
            elif j > jj:
                for jjj in range(jj, j):
                    if grid[i][jjj] != '.':
                        return False
            for iii in range(i+1, ii):
                if grid[iii][jj] != '.':
                    return False

        elif i > 1 and ii == 1: # other L-route
            if j < jj:
                for jjj in range(j+1, jj+1):
                    if grid[ii][jjj] != '.':
                        return False
            elif j > jj:
                for jjj in range(jj, j):
                    if grid[ii][jjj] != '.':
                        return False
            for iii in range(ii, i):
                if grid[iii][j] != '.':
                    return False

        elif i > 1 and ii > 1: # U-route
            if j < jj:
                for jjj in range(j+1, jj+1):
                    if grid[1][jjj] != '.':
                        return False
            elif j > jj:
                for jjj in range(jj, j):
                    if grid[1][jjj] != '.':
                        return False
            for iii in range(1, i):
                if grid[iii][j] != '.':
                    return False

            for iii in range(1, ii+1):
                if grid[iii][jj] != '.':
                    return False

        return True


    def legal_moves(grid):
        for move in potential_moves(grid):
            if legal_move(move, grid):
                yield move

    def adjacent_states(u):
        grid0 = state_to_grid(u, nodes, grid)
        for mv in legal_moves(grid0):
            grid1 = deepcopy(grid0)
            weight = move( *mv, grid1)
            v = grid_to_state(nodes, grid1)
            yield v, weight



    start = grid_to_state(nodes, grid)

    grid_end = deepcopy(grid)
    for k, v in columns.items():
        for i in range(2, m-1):
            grid_end[i][v] = k
    end = grid_to_state(nodes, grid_end)

    def heuristic(u):
        return 0
        grid0 = state_to_grid(u, nodes, grid)
        res = 0
        inplace = defaultdict(int)
        out_of_place_in_column = defaultdict(int)
        for k, j in columns.item():
            for i in range(m-2, 1, -1):
                if grid0[i][j] == k:
                    inplace[k] += 1
                else:
                    break

        for k, j in columns.item():
            for i in range(m-2-inplace[k], 1, -1):
                if grid0[i][j] == k:
                    out_of_place_in_column[k] += 1


        

        for i in range(m):
            for j in range(n):
                token = grid0[i][j]

                if grid0[i][j] in 'ABCD':
                    if columns[token] == j:
                        pass
                    res += 1
        return res

    dist = { start : 0 }
    came_from = { start : None }

    q = [ (0, start) ]
    heapq.heapify(q)

    count = 0
    while q:
        if count % 10000 == 0:
            print(count, len(q), q[0][0], ''.join(q[0][1]))
        count += 1
        _, u = heapq.heappop(q)
        if u == end:
            break
        for v, weight in adjacent_states(u):
            alt = dist[u] + weight
            if v not in dist or alt < dist[v]:
                dist[v] = alt
                priority = alt + heuristic(v)
                heapq.heappush(q, (priority, v))
                came_from[v] = u

    assert end in dist
    print(count, len(q), dist[u], ''.join(u))

    u = end
    path = [u]
    while u != start:
        u = came_from[u]
        path.append(u)
    path.reverse()

    for u in path:
        grid0 = state_to_grid(u, nodes, grid)
        prnt(grid0)
        print()

    return dist[end]

def xtest_A():
    txt = \
"""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
    print(main(txt))

def xtest_B():
    txt = \
"""#############
#...........#
###D#A#D#C###
  #C#A#B#B#
  #########
"""
    print(main(txt))

def xtest_AA():
    txt = \
"""#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
"""
    print(main(txt))

def test_BB():
    txt = \
"""#############
#...........#
###D#A#D#C###
  #D#C#B#A#
  #D#B#A#C#
  #C#A#B#B#
  #########
"""
    print(main(txt))