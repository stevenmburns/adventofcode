
def gen0():
    id = (yield)
    print(f'Start {id}')
    while True:
        x = (yield)
        print( f'unit {id} read {x}')
        yield x+1


def chain():

    xs = [ gen0() for i in range(3)]

    for idx, x in enumerate(xs):
        next(x)
        x.send(idx)

    v = 0
    for outer in range(4):
        for inner in range(3):
            v = xs[inner].send(v)
            print(f'outer {outer} inner {inner} v {v}')
            next(xs[inner])


def test_B():
    chain()
