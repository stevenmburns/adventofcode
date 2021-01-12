import pytest
import io
import re

def parse(fp):

    seq = []

    for line in fp:
        line = line.rstrip('\n')
        nums = [ int(x) for x in line.split('\t')]
        seq.append(nums)

    return seq

def main(fp):
    seq = parse(fp)
    
    sum = 0
    for nums in seq:
        m, M = None, None
        for x in nums:
            if m is None or m>x: m = x
            if M is None or M<x: M = x
        sum += M - m
        
    return sum

def main2(fp):
    seq = parse(fp)
    
    sum = 0
    for nums in seq:
        for i in range(len(nums)):
            for j in range(len(nums)):
                if i == j: continue
                x,y = nums[i],nums[j]
                if x % y == 0:
                    sum += x // y
        
    return sum

#@pytest.mark.skip
def test_A():
    with open('data0', 'rt') as fp:
        assert 18 == main(fp)

def test_AA():
    with open('data1', 'rt') as fp:
        assert 9 == main2(fp)

#@pytest.mark.skip
def test_B():
    with open('data', 'rt') as fp:
        print(main(fp))

#@pytest.mark.skip
def test_BB():
    with open('data', 'rt') as fp:
        print(main2(fp))

