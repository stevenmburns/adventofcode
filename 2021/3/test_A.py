def parse(fp):
    for line in fp:
        line = line.rstrip('\n')
        yield line

def main(fp):
    lst = list(parse(fp))

    m = len(lst)
    n = len(lst[0])

    ones = [sum(1 for i in range(m) if lst[i][j] == '1') for j in range(n)]
    zeroes = [sum(1 for i in range(m) if lst[i][j] == '0') for j in range(n)]


    gamma_str = ''.join( '1' if ones[i] > zeroes[i] else '0' for i in range(n))

    epsilon_str = ''.join( '0' if ones[i] > zeroes[i] else '1' for i in range(n))

    return int(gamma_str, 2) * int(epsilon_str, 2)

def main2(fp):
    lst = list(parse(fp))
    n = len(lst[0])

    def restrict( lst, j, tag):

        m = len(lst)

        ones = [x for x in lst if x[j] == '1']
        zeroes = [x for x in lst if x[j] == '0']
        
        if tag == 'oxygen':
            return ones if len(ones) >= len(zeroes) else zeroes
        else:
            return ones if len(ones) < len(zeroes) else zeroes

    oxygen_lst = lst
    for j in range(n):
        #print(oxygen_lst, 'before')
        oxygen_lst = restrict(oxygen_lst, j, 'oxygen')
        #print(oxygen_lst, 'after')
        if len(oxygen_lst) == 1:
            break

    assert len(oxygen_lst) == 1


    co2_lst = lst
    for j in range(n):
        co2_lst = restrict(co2_lst, j, 'co2')
        #print(co2_lst)

        if len(co2_lst) == 1:
            break 
    
    assert len(co2_lst) == 1

    print(oxygen_lst, co2_lst)

    return int(co2_lst[0], 2) * int(oxygen_lst[0], 2)


def test_A0():
    with open("data0") as fp:
        assert 198 == main(fp)

def test_B():
    with open("data") as fp:
        assert 1082324 == main(fp)

def test_AA0():
    with open("data0") as fp:
        assert 230 == main2(fp)

def test_BB():
    with open("data") as fp:
        print(main2(fp))