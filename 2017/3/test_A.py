import pytest
import io
import re

def main(n):
        
    def f(i):
        return (1 + i*2)**2
    layers = 0
    while f(layers) < n:
        layers += 1

    if layers == 0:
        assert n == 1
        return 0

    lb = f(layers-1)+1
    ub = f(layers)+1

    assert (ub-lb) % 4 == 0
    
    pos = (n-lb) % (2*layers) - layers + 1

    print( n, layers, pos)

    return layers + abs(pos)


#@pytest.mark.skip
def test_A0():
    assert 0 == main(1)
def test_A1():
    assert 3 == main(12)
def test_A2():
    assert 2 == main(23)
def test_A3():
    assert 4 == main(25)
def test_A4():
    assert 5 == main(26)
#@pytest.mark.skip
def test_A5():
    assert 31 == main(1024)

#@pytest.mark.skip
def test_B():
    print(main(277678))

