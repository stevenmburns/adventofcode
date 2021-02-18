
def test_A():
    def gen():
        for i in range(3):
            x = (yield)
            print(x)
            x += 1; yield x
            x += 1; yield x


    g = gen()
    assert next(g) is None

    assert 1 == g.send(0)
    assert 2 == g.send(1000) # 1000 dropped

    assert g.send(1000) is None # 1000 dropped
    assert 11 == g.send(10)
    assert 12 == g.send(1000)

    assert next(g) is None
    assert 21 == g.send(20)
    assert 22 == g.send(1000)

    try:
        next(g)
    except StopIteration:
        pass
    else:
        assert False
