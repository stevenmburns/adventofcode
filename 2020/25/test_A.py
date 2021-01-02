
import io
import pytest

import logging
from logging import debug
import re

import re
import collections
from collections import deque

def parse(fp):
    seq = []

    for line in fp:
        line = line.rstrip('\n')
        seq.append(int(line))

    return seq

def transform( subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value

def inverse( subject_number):
    result = None
    for i in range(1,20201227):
        if (i*subject_number) % 20201227 == 1:
            result = i
            break
    return result

def solve( public_key, subject_number_inverse):
    result = None
    value = public_key
    for i in range(1,20201227):
        value = (value*subject_number_inverse) % 20201227
        if value == 1:
            result = i
            break
    return result


def gen_card_public_key( card_secret_loop_size):
    result = transform( 7, card_secret_loop_size)
    return result

def gen_door_public_key( door_secret_loop_size):
    return transform( 7, door_secret_loop_size)

def main( fp):
    inverse_of_7 = inverse(7)

    card_public_key, door_public_key = tuple(parse(fp))

    card_secret_loop_size = solve( card_public_key, inverse_of_7)
    door_secret_loop_size = solve( door_public_key, inverse_of_7)

    encryption_key0 = transform( door_public_key, card_secret_loop_size)
    encryption_key1 = transform( card_public_key, door_secret_loop_size)
    
    assert encryption_key0 == encryption_key1

    return encryption_key0

def test_A():
    with open("data0", "rt") as fp:
        assert 14897079 == main(fp)

def test_C():
    with open("data", "rt") as fp:
        print(main(fp))
