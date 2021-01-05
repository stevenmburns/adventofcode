def main(txt):
    board = txt.split('\n')

    def b( r, c):
        assert 0 <= r < len(board)
        assert 0 <= c

        ncols = len(board[0])

        return board[r][c%ncols] == '#'


    sum = 0
    for r in range(len(board)):
        if b( r, 3*r):
            sum += 1

    print(sum)

def main2(txt):
    board = txt.split('\n')

    def b( r, c):
        assert 0 <= r < len(board)
        assert 0 <= c

        ncols = len(board[0])

        return board[r][c%ncols] == '#'


    def trees( delta_r, delta_c):
        sum = 0
        for r in range(0,len(board),delta_r):
            if b( r, delta_c*r//delta_r):
                sum += 1
        return sum

    result = trees( 1, 1) * trees( 1, 3) * trees( 1, 5)  * trees( 1, 7)  * trees( 2, 1) 

    print( result)



def test_A():
    txt = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    main(txt)
    main2(txt)


def test_B():
    txt = """....#...##......##..#..#.#...#.
..######...#......#....#..#.##.
..#.#...##......#.#..#..#....#.
..#.....#..#.#........#.#..#..#
#......##..###...#.#..#.....#..
#.......##...###...#....#......
.....##...#......##.#.#..#.##..
.........#......#.....#......#.
..#.#..#....#....#......##.#.##
.#...#..#.............#.#..#.#.
....#..#.#.##.#....#..#..#....#
...#..#.....#.......#...#..#..#
.....#.....#.......#..#...#....
.##.......#...#..#........#...#
...#.......#.#.#...#.#.#......#
#....#..#.....#......##....#..#
###.#......#.#.#.#..#....#....#
......##......#.#...#...#..#...
.....#......#.#.#......#.#.....
...##...#..#........#..#.##....
..##.#.#..#...###..........#.#.
.#..#..#.....#.........#.###.#.
....##.....#...#...##..#.##...#
....#.##....#.....##......#....
........#.#.........#.#.......#
#....##.#....#..#...#..........
#..###......#....##..........##
....##.#.....#..#.##......#....
#..#......#......#.............
...##.....##.......#.......#...
#...#.#.....#..........#...###.
#.....#..#.#.###...#......###..
...##.#......#........#..#.....
......#.....###.#...##........#
.#......##......##....#....#...
..#.#..#.....##....#....#..#...
..#.#.....#.##.#.....#.....#...
....#.......#...#.........##...
.#....#..#.......##.......#....
..#..##.....#...##.##.#.#......
.##.#....#............#.......#
.......#...#..#.#.##.....##..##
..###....#..#.##........##.#...
....#.#..#.....#..#.#.....#....
..#..#.#..............#..#.....
.......#.#.#.........#......#..
...##..#.#...#......##.#.......
#....#.#.........#...#....#..##
.#..#.#...#.......#.#.#....#.##
.#..###.#..#.#.....#..#........
#.#..##.###.....##.........#..#
#...##...#..##..#..#..........#
.#...#..#......................
...##..###...........#.#...##..
..........#.#....#.#...........
..#....#....#..#....#.#.#......
.#..#.....###......#...#...#...
#.##..#..#.........#..#....#...
........#......#...#.........#.
..#.....#.#..##...#.#.#...##...
..#...........#.##..#.#..#.##..
..............##...#.#......#..
#.#..#....#...##.###........#..
.#...#..#........#........##..#
.....##..#...#.....#.#.........
.#...#...#....###...#.#.#..##..
....#.........#....###..##....#
.#....#...####...##....####.#..
..#..#.......#..#......#.#.#...
....#....#.......##..#.#.......
..#....#...........##.#.##.....
#..#..#...##.##....#.#.#.###.##
...#...#....#.#...##...#....###
......##........#.........#.#..
....#####..#..##.......#.#....#
....##..#...###....#..#.....#..
..#........#..#.#.....#....#...
..#....#......#..#...#......#..
...#.....##...#.#..##.....#..#.
...#..#.......####.##...#......
.....#..#..#.##..##....#..#.#..
..#..#..##.#.#.##..#..#...#....
...#..........#.........#....##
.##.....###...............#.##.
...##...........#.#.#......#..#
.#...#.#.##....#....#..#.......
.#...###.#....#..#..#..#......#
#..#........###...........#..#.
..#...#......#.#.#......####.#.
...#.#....##.#.....#.....##....
...###..#.#.#...#.....#.###..#.
.#.#..#...##......#..........#.
##.....#.......#.#..###...#.#..
##.###....#.....#.....###.#....
#...#..##....#.#...#...#......#
.....##.#........#.###.........
.#..#..#.#......##.#...#.#.....
#..#.#........##...........##.#
#...###..#..####..#.#..........
..#...#....#...##.#....#....##.
......#.#........#.....#..#....
#.........#...#.....#...#..##..
#....#.........#...#.##..###.#.
#...###...#.##.#.#.............
#.#....#....#......#....#.#...#
##...#.##......#..#.#....#.....
....#...#.##....#..............
.........##..........#..##..#..
......##....#.#......#.........
..#.#..............#......#..##
...........##.......#.#.#......
##...#........##.......#.#.....
....#...#...#....#.#......##...
...#..#.#.#.........#..#.#....#
.##.#...#.#.........#.....##.#.
#.#.....#.#.....#..............
..#.#..#....#..........#..##...
...#..#....................#..#
...........#...........#...#..#
............#...#............##
..#....##......##...........#..
..#..#..#....#....##......##.##
##..........#..##.##.#...#.....
............#..#........###.#..
###...##.#.#....#....#.#....#..
...#......##...#.......####....
.......#..#..#.#.....#.........
........##.......##.....#......
#.#...#.###....#..#...##.......
...#.#....#..#####.#..##.#.....
..#.#..##.......###...#.....#..
..#.......#..#...#...#..#.##...
......#..#.......#.....#....#..
.......#........#.#.......##..#
.#.#.....#.......#.......##..#.
..#.#....#.#.#####.....#...#...
#..#............###.......#..#.
........##.........#..#...###..
.#............##...#.....#.....
.#..##..#....#....#.......#....
....##..........##.............
.##..........#..#..#....#...#..
...#..#..#............####.....
.............#..#.##..#.#.##...
.....#........#....#.#.......#.
###.#..#.#...#....##...........
....#......#...#....##.......#.
.......#.#...#.#...#........##.
..........#........#..#.##.....
##..#.#.....##.#...............
.....#....#................#...
...##....#........##.#....#....
.....##...###....#.#..#.......#
.....#.#.........##....###.....
.#.....##......#..##..##...##.#
.#..............#.....#.#......
.##......#..#..#......##.......
.......#..................#....
...#.#...##......####.........#
#....#####.#.#..#..#..#...#...#
##.#...#.......#....#...#...###
...#........#.....#...#.##.....
..##....#.......#....#.......##
#......#..##...#..##.#.....#.#.
..###........#.#..#........#.#.
...#.###..........#.....#.#.#..
#.###.....#...#...#..##..###...
#....#.#.....#.#........#......
........#.......##.......#.....
...........#...#......##.......
............#...#....#..#.....#
#.#.#.#....#.....#.#..........#
#.##...#...#..#....##.#.......#
...#..#......#..#...##..##..#..
#....#......#.#.....##.#..#....
#....#..##.#......#.#.....#..##
.#..##....##....#.#...#...#....
#.#.###....#.#............#...#
.#.#....#..#..........#....#.#.
......#..#.#...............##..
..#......###.#..........#.###..
....#.##.#..#...##..#.#...#....
..............#...##.......#.##
.#...........#....#....#.##....
#..#....#.....#...#.....##...#.
.........#...#.##.......#...#.#
.....#......#.........#.#..#...
##..........#.#..##...#.#.#....
##..##.#..#..#.....#.##....#...
........##....#.#.#....#......#
.#.##...#.###....#.........#..#
..........#....###..#.........#
#.#..#.#...#.......#..##.......
..#....#...###..............##.
#..###.....####...#..#..#...#..
......#..#...###........###....
..#.....#...#.......#....###..#
.#.........#.#.#....#.#.......#
#.#.###.#.#...........#........
......#..#.........#........#..
...........##.#........#.#...#.
.....#.#......##.......#.....##
...##...#............#..#.....#
.....#..##....##...##.#..#.#...
...#...#........#.#......##....
........#..##..#..#......##.#..
.#.#.....#.....#...........#.##
.#...#.#............#......#...
.....#...#........#....#..#.#..
...##....#..#...#..............
#....##.#.#............#.......
#..#..#.....##..#........##.#.#
##..#.#....#....##.......###..#
.#.#.#.....###.....#.#......###
.....#..#...###...#....#.#...#.
.##.....................##....#
.#.....#.........#....#.....##.
#...#....#.#...###.......#.#..#
...#.................#.#....#.#
.##...#.#......................
.##.#........#...##............
.#....#.....#.........#.##..##.
#......#...##..#.........##.##.
......#......#...####..#.##....
.###....#..##......#.##......#.
..#...#....#..#.......#.#......
#....#...#.................#.#.
....#.#.#..#...#..#.......#.#.#
#.#...##.......#.....##.#......
#.........#.....##..##..#......
....#..##..#.....#..#..#.#..#..
......#.#..#.#.#....#.#.......#
.##......#..#....##...##..#....
..#..#......#...##..#.##.....#.
..#..#.......#.#....#.....#...#
....#.#.....###...#.......#.#..
..#....##.....##.#........##...
#...............##....#.....##.
.#.........#....#...##.###.##.#
.#.##..#.............#.#.#..#..
.#.....#.................##....
..####.........#.#......#.#..#.
#.......#..........#.#........#
.#.#...##.....#.#.......#....#.
..#.##.#.......###....#....#...
.#....##.............##.#.#.#..
#.#.....#.#.#.#..#......##..#..
.............#..........#.#.#..
...#.#.............#.#...##....
.......#..#.#.......#..#.#....#
.............#.........###..#..
.#.#..#....#.....#..#.....#...#
#.....#....##..##.#..#........#
..##..###.....##....#.#..#.....
..#...##....#...#.#..........#.
...##..##.#.....#....#.........
..#...#........##.#..#........#
#.............#.###......#.##..
.#...#........#...........#...#
..##.......#.#..##.##......#...
...#.#...##....##..#...........
.#......##........#....##....#.
.........#..#....#...#..##.##..
....#..#.#...#.......#.#.##....
...#.#......#.#..#..#.#....#..#
.......#........#.........###..
#.#..#.#.........##............
##..##..#.##..###...#.#...#....
.#....#.#..#...#....#.##.....#.
.#.#.#.#........##...#..#.#.##.
.#..#.#..#...........#..#......
..#.##.#...#....#.........#...#
.....##...#.#...#...#....#.....
..#..........#.#.#.......##.#..
#.#............#..#.....#..#...
..#...........##.#.##.#....#..#
#..####.....#............#.....
.##......#####.#..#.....#....#.
...##..#.#......#.#..#..#...##.
#....................#.##...#.#
...#............#.............#
....#.##..........#.....#......
....##..##....#.#..............
...........#....##.#.....#.....
....#.....#....#....#......#...
#...##........#...#........#.#.
........#.....##..#.##.#..#.#.#
....##......##....#.....##....#
...#.#........##.......#...##..
#......##..#.#.#....##......#..
..#.......#.......##..#.##.....
.#...#...#.#.............##....
......#.#.#.........##...#..#.#
.....#..####....#.##..........#
...#...#.#....#.....#..#.....##
.........#.......#......###....
........##..##..#.#.#...###...#
.#..##.#....#...##.....#.#.#...
........##...#...##..#.........
.........#.......#.##..#...####
#......#.....#..............#.#
##..##.#.##.....##...........#.
#.............#.........#......
...####.#.##..#.#.#.##.#......#
..#.....##....#...#............
#..............#......#...###..
..#..#.#...#.##.........##.....
..#...##..#........#..#.##..##.
......###...#..#....#..#.###...
...##.##.###.....##.#.......#..
#....#..###..#.......#.#.#..#..
..##.............##..##...###.#
.#.#..#.........#..........#...
.........#.#.....##...#..#...##
....#..#....#####..#...#..#....
...#.....#.....#...#.#..#.#....
.#..#.............#.......##.#.
...##.......#.#.....##......#..
...........##..#.##..###...#.#.
...........#...........#...#..#
..#....#.##.#..#..#...........#
..#.....##...#......#...#......
...###.###.....##..........#..#"""

    main(txt)
    main2(txt)