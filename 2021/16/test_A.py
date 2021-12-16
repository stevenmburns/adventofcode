import pytest
import io
from functools import reduce

def parse(fp):
    tbl = {}
    for i in range(16):
        code = []
        for j in reversed(range(4)):
            if i & (1 << j) != 0:
                code.append('1')
            else:
                code.append('0')
        
        tbl[hex(i)[2:].upper()] = ''.join(code)


    for line in fp:
        line = line.rstrip('\n')
        for x in line:
            yield from tbl[x]

def parse_packet(bits, i):
    version_sum = int(bits[i:i+3], 2)
    i += 3
    typeID = int(bits[i:i+3], 2)
    i += 3
    if typeID == 4:
        l = []
        while True:
            exit = bits[i] == '0'
            i += 1
            l.append(bits[i:i+4])
            i += 4
            if exit:
                break
        return i, version_sum, int(''.join(l), 2)
    else:
        lengthTypeID = int(bits[i:i+1], 2)
        i += 1
        fields = []
        if lengthTypeID == 0:
            total_length = int(bits[i:i+15], 2)
            i += 15
            ii = i
            while ii + total_length != i:
                assert ii + total_length > i
                i, version, field = parse_packet(bits, i)
                version_sum += version
                fields.append(field)
        else:
            number_of_sub_packets = int(bits[i:i+11], 2)
            i += 11
            for _ in range(number_of_sub_packets):
                i, version, field = parse_packet(bits, i)
                version_sum += version
                fields.append(field)

        if typeID == 0:
            field = sum(fields)
        elif typeID == 1:
            field = reduce(lambda x, y: x * y, fields)
        elif typeID == 2:
            field = min(fields)
        elif typeID == 3:
            field = max(fields)
        elif typeID == 5:
            assert len(fields) == 2
            field = 1 if fields[0] > fields[1] else 0
        elif typeID == 6:
            assert len(fields) == 2
            field = 1 if fields[0] < fields[1] else 0
        elif typeID == 7:
            assert len(fields) == 2
            field = 1 if fields[0] == fields[1] else 0
        else:
            assert False, f'Unknown typeID: {typeID}'
        return i, version_sum, field

def main(fp):
    bits = ''.join(parse(fp))

    i, sum_of_version_numbers, _ = parse_packet(bits, 0)
    assert all(x == '0' for x in bits[i:])

    return sum_of_version_numbers

def main2(fp):
    bits = ''.join(parse(fp))

    i, _, field = parse_packet(bits, 0)
    assert all(x == '0' for x in bits[i:])

    return field
    

def test_A0():
    with open('data0') as fp:
        assert 6 == main(fp)


def test_A2():
    with io.StringIO('8A004A801A8002F478') as fp:
        assert 16 == main(fp)

def test_A3():
    with io.StringIO('620080001611562C8802118E34') as fp:
        assert 12 == main(fp)

def test_A3():
    with io.StringIO('C0015000016115A2E0802F182340') as fp:
        assert 23 == main(fp)

def test_A4():
    with io.StringIO('A0016C880162017C3686B18A3D4780') as fp:
        assert 31 == main(fp)

def test_B():
    with open('data') as fp:
        print(main(fp))

def test_AA2():
    with io.StringIO('C200B40A82') as fp:
        assert 3 == main2(fp)

def test_AA3():
    with io.StringIO('04005AC33890') as fp:
        assert 54 == main2(fp)

def test_AA4():
    with io.StringIO('880086C3E88112') as fp:
        assert 7 == main2(fp)

def test_AA5():
    with io.StringIO('CE00C43D881120') as fp:
        assert 9 == main2(fp)

def test_AA6():
    with io.StringIO('D8005AC2A8F0') as fp:
        assert 1 == main2(fp)

def test_AA7():
    with io.StringIO('F600BC2D8F') as fp:
        assert 0 == main2(fp)

def test_AA8():
    with io.StringIO('9C005AC2F8F0') as fp:
        assert 0 == main2(fp)

def test_AA9():
    with io.StringIO('9C0141080250320F1802104A08') as fp:
        assert 1 == main2(fp)

def test_BB():
    with open('data') as fp:
        print(main2(fp))
