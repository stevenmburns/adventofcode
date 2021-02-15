#from util import get_data
import re
from collections import defaultdict
import pytest

from z3 import *

def gan(s):
  return list(map(int, re.findall(r'-?\d+', s)))

def lenr(l):
  return range(len(l))

def parse(fp):
    seq = []

    p = re.compile(r'^pos=<((|-)\d+),((|-)\d+),((|-)\d+)>, r=(\d+)$')
    for line in fp:
        line = line.rstrip('\n')
        m = p.match(line)
        assert m
        seq.append( ( (int(m.groups()[0]),int(m.groups()[2]),int(m.groups()[4])), int(m.groups()[6])))

    return seq

def main(fp):
  nanobots = parse(fp)

  def zabs(x):
    return If(x >= 0,x,-x)
  (x, y, z) = (Int('x'), Int('y'), Int('z'))
  in_ranges = [
    Int('in_range_' + str(i)) for i in lenr(nanobots)
  ]
  range_count = Int('sum')
  o = Optimize()
  for i in lenr(nanobots):
    (nx, ny, nz), nrng = nanobots[i]
    o.add(in_ranges[i] == If(zabs(x - nx) + zabs(y - ny) + zabs(z - nz) <= nrng, 1, 0))
  o.add(range_count == sum(in_ranges))
  dist_from_zero = Int('dist')
  o.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
  h1 = o.maximize(range_count)
  h2 = o.minimize(dist_from_zero)
  print (o.check())
  print ("b", o.lower(h2), o.upper(h2))

@pytest.mark.skip
def test_A():
    with open("data0","rt") as fp:
        assert 7 == main(fp)

#@pytest.mark.skip
def test_B():
    with open("data","rt") as fp:
        print(main(fp))
