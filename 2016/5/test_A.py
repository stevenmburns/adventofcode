import pytest
import io
import re
import hashlib

def main(txt):
    idx = 0
    password = ''
    while len(password) < 8:
        base = f'{txt}{idx}'
        hexstr = hashlib.md5(base.encode()).hexdigest()
        if hexstr[:5] == '00000':
            password += hexstr[5]
        idx += 1

    return password

def main2(txt):
    def hexchar2int( c):
        if c in '0123456789':
            return ord(c) - ord('0')
        elif c in 'abcdef':
            return 10 + ord(c) - ord('a')            
        else:
            assert False

    idx = 0
    password = {}
    while len(password) < 8:
        base = f'{txt}{idx}'
        hexstr = hashlib.md5(base.encode()).hexdigest()
        if hexstr[:5] == '00000':
            position = hexchar2int(hexstr[5])
            if position < 8:
                if position not in password:
                    password[position] = hexstr[6]
        idx += 1

    return ''.join( password[i] for i in range(8))


def test_A():
    #assert '18f47a30' == main('abc')
    assert '05ace8e3' == main2('abc')


def test_B():
    #print(main('abbhdwsy'))
    print(main2('abbhdwsy'))
