import pytest
import io
import re
import itertools
from collections import defaultdict
import logging

#logging.basicConfig(level=logging.INFO)

def main(*,depth,target):
    MX, MY = target

    gi_memo = { (0,0): 0, target: 0}

    def gi( p):
        if p in gi_memo:
            return gi_memo[p]
        else:
            x,y = p
            if x == 0:
                cand = y*48271
            elif y == 0:
                cand = x*16807
            else:
                cand = el((x-1,y)) * el((x,y-1))
            gi_memo[p] = cand
            return cand

    def el( p):
        return (gi(p) + depth) % 20183

    def ty( p):
        return el(p) % 3

    sum = 0
    for x in range(0,MX+1):
        for y in range(0,MY+1):
            sum += ty( (x,y))


    # tier 0 means neither torch or climbing gear
    # tier 7 means torch
    # tier 14 means climbing gear
    # tiers run from 0 to 20 (the one after 20 is 0)

    neither = 0
    torch = 7
    climbing_gear = 14

    def safe( tier, ty):
        return ty == 0 and tier in [torch,climbing_gear] or \
               ty == 1 and tier in [neither,climbing_gear] or \
               ty == 2 and tier in [torch,neither]
        
    next_tier_tbl = { ( neither, -1) : climbing_gear,
                      ( neither,  1) : torch,
                      ( torch,   -1) : neither,
                      ( torch,    1) : climbing_gear,
                      ( climbing_gear, -1) : torch,
                      ( climbing_gear,  1) : neither}

    def gen_adjacent( t):
        (x,y), tier = t
        dirs = [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]
        for dx,dy,dtier in dirs:
            xx = x+dx
            yy = y+dy
            ntier = (tier+dtier)%21
            if xx < 0 or yy < 0: continue
            if xx > target[0]+50 or yy > target[1]+50: continue
            if safe( ntier, ty( (xx,yy))) and safe( tier, ty( (x,y))):
                yield (xx,yy),ntier
            elif dx == 0 and dy == 0:
                # Ensure we are moving toward a legal solution
                cand = (tier, dtier)
                if cand not in next_tier_tbl or safe( next_tier_tbl[cand], ty( (x,y))):
                    yield (xx,yy),ntier

    reached = set()
    frontier = { ((0,0),torch)}

    minutes = 0
    while frontier:
        print(minutes,len(reached),len(frontier))
        if (target,torch) in frontier:
            break
        new_frontier = set()
        for t in frontier:
            logging.info( f'{t}')
            for tt in gen_adjacent(t):
                logging.info( f'\t{tt}')
                new_frontier.add(tt)
        reached = reached.union(frontier)
        frontier = new_frontier.difference(reached)
        minutes += 1

    return sum, minutes

@pytest.mark.skip
def test_A():
    assert (114,45) == main(depth=510,target=(10,10))

#@pytest.mark.skip
def test_B():
    print(main(depth=9465, target=(13,704)))
