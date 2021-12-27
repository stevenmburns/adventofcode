
from copy import deepcopy

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
        token = grid[i][j]
        grid[ii][jj] = token
        grid[i][j] = '.'

        prnt(grid)

        if i > 1 and ii > 1:
            dist = i-1 + ii-1 + abs(j-jj)
        else:
            dist = abs(i-ii)+abs(j-jj)

        cost = dist * costs[token]

        print( f'----{cost}----')

        return cost

    state = grid_to_state(nodes, grid)

    grid0 = state_to_grid(state, nodes, grid)

    cost = 0
    cost += move( 2, 9, 1, 10, grid0)
    cost += move( 3, 9, 1, 1, grid0)
    cost += move( 2, 3, 1, 2, grid0)
    cost += move( 4, 9, 1, 7, grid0)
    cost += move( 5, 9, 1, 8, grid0)
    return cost
    cost += move( 1, 10, 5, 9, grid0)
    cost += move( 1, 8, 1, 11, grid0)
    cost += move( 1, 7, 1, 10, grid0)
    cost += move( 3, 3, 4, 9, grid0)
    cost += move( 4, 3, 3, 9, grid0)
    cost += move( 1, 2, 1, 4, grid0)
    cost += move( 1, 1, 4, 3, grid0)
    cost += move( 1, 4, 1, 1, grid0)
    cost += move( 2, 5, 1, 2, grid0)
    cost += move( 3, 5, 1, 3, grid0)
    cost += move( 4, 5, 1, 4, grid0)
    cost += move( 5, 5, 2, 9, grid0)
    cost += move( 1, 4, 5, 5, grid0)
    cost += move( 2, 7, 4, 5, grid0)
    cost += move( 3, 7, 3, 5, grid0)
    cost += move( 4, 7, 1, 6, grid0)
    cost += move( 1, 10, 4, 7, grid0)
    cost += move( 1, 6, 1, 8, grid0)
    cost += move( 1, 3, 3, 7, grid0)
    cost += move( 1, 2, 2, 7, grid0)
    cost += move( 1, 1, 2, 5, grid0)
    cost += move( 1, 8, 3, 3, grid0)
    cost += move( 1, 11, 2, 3, grid0)

    return cost

    state0 = grid_to_state(nodes, grid0)

    grid1 = state_to_grid(state0, nodes, grid)

    prnt(grid1)


    return cost

def test_AA():
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

def xtest_BB():
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