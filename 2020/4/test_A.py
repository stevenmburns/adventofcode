
import io

import logging
from logging import debug
import re

logging.basicConfig(level=logging.DEBUG)

p_yr = re.compile(r"^(\d\d\d\d)$")
p_hgt = re.compile(r"^(\d+)(cm|in)$")
p_hcl = re.compile(r"^#[a-f0-9]{6}$")
p_pid = re.compile(r"^\d{9}$")

def year_in_range(v, lb, ub):
    m = p_yr.match(v)
    if m:
        yr = int(m.groups()[0])
        return lb <= yr <= ub
    else:
        return False

def valid_hgt( v):
    m = p_hgt.match(v)
    if m:
        value = int(m.groups()[0])
        units = m.groups()[1]
        debug( f"valid_hgt: {value} {units}")
        if units == "in":
            return 59 <= value <= 76
        else:
            return 150 <= value <= 193
    else:
        return False

def validate( k, v):
    if k == "byr":
        return year_in_range( v, 1920, 2002)
    if k == "iyr":
        return year_in_range( v, 2010, 2020)
    if k == "eyr":
        return year_in_range( v, 2020, 2030)
    if k == "hgt":
        return valid_hgt( v)
    if k == "hcl":
        return p_hcl.match(v)
    if k == "ecl":
        return v in ["amb","blu","brn","gry","grn","hzl","oth"]
    if k == "pid":
        return p_pid.match(v)
    if k == "cid":
        return True
    return False

def main( fp):
    records = []

    record = []
    for line in fp:
        line = line.rstrip('\n')
        if line == '':
            records.append(record)
            record = []
        else:
            record.extend(line.split(' '))
    records.append(record)    

    records = [ dict([ tuple(x.split(':')) for x in record]) for record in records]

    required = { "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    optional = { "cid"}
    required_union_optional = required.union(optional)

    count = 0
    for record in records:
        debug( "="*80)
        legal = True
        for (k,v) in record.items():
            if k not in required_union_optional:
                debug( f"Failed1: {k}")
                legal = False
            else:
                if not validate(k,v):
                    debug( f"Failed validate: {k} {v}")
                    legal = False
        for k in required:
            if k not in record:
                debug( f"Failed2: {k} {record}")
                legal = False
        if legal:
            count += 1

    return count

def test_A():
    fp = io.StringIO( """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""")

    assert 2 == main(fp)

def test_B():
    with open( "data", "rt") as fp:
        print(main(fp))
    
