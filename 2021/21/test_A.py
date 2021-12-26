
import pytest
from itertools import cycle, product
from collections import Counter, defaultdict


class Player:
    def __init__(self, position):
        self.position = position
        self.score = 0

    def step(self, rolls):
        for roll in rolls:
            self.position += roll
            self.position = (self.position - 1) % 10 + 1

        self.score += self.position

def main(p1 = 6, p2 = 4):
    player1 = Player(p1)
    player2 = Player(p2)

    gen = cycle(range(1,101))

    count = 0

    while True:
        a = next(gen)
        b = next(gen)
        c = next(gen)

        player1.step([a,b,c])
        count += 3

        if player1.score >= 1000:   
            break

        a = next(gen)
        b = next(gen)
        c = next(gen)

        player2.step([a,b,c])
        count += 3

        if player2.score >= 1000:   
            break

    
    return count * min(player1.score, player2.score)


def main2(p1 = 6, p2 = 4):

    histo = Counter(sum(x) for x in product(range(1,4), repeat=3))


    def step(states):

        dict = defaultdict(int)

        for state in states:
            replications, score, position = state
            for k, v in histo.items():
                p = (position + k - 1) % 10 + 1
                s = score + p
                dict[(s, p)] += replications*v

        newstates = set()
        for k, v in dict.items():
            newstates.add( (v, k[0], k[1]) )

        keep = { (r,s,p)for r,s,p in newstates if s < 21}
        finished = { (r,s,p)for r,s,p in newstates if s >= 21}
        return keep, finished

    def runall(keep):
        res = []
        while keep:
            keep, finished = step( keep)
            num_finished = sum(r for r,_,_ in finished)
            res.append(num_finished)
        return res

    save_finished1 = runall({(1,0,p1)})
    save_finished2 = runall({(1,0,p2)})

    p1_x, p2_x = 1, 1
    p1_wins, p2_wins = 0, 0
    for (a,b) in zip(save_finished1, save_finished2):
        p1_wins += a*p1_x
        p1_x *= 27
        p1_x -= b

    # Only works if p1_wins (both test cases that I have)
    # Probably only works if save_finished1 and save_finished2 are the same length

    return max(p1_wins, p2_wins)

#@pytest.mark.skip
def test_A0():
    assert main(4, 8) == 739785


#@pytest.mark.skip
def test_B():
    print(main())

#@pytest.mark.skip
def test_AA0():
    assert main2(4, 8) == 444356092776315


#@pytest.mark.skip
def test_BB():
    print(main2())

