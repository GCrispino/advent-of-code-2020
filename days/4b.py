import re

expr = re.compile(r"\n|\s")


def parse_passport(pass_string):
    entries = expr.split(pass_string)
    return {(spl:= e.split(':'))[0]: spl[1] for e in entries}


def get_passports(text_input):
    passports = text_input.split('\n\n')
    final_passports = [parse_passport(p.strip()) for p in passports]
    return final_passports


def is_passport_valid(passport, required_fields):
    return all([(field in passport) and validator(passport[field]) for field, validator in required_fields])


def validate_height(v):
    expr = re.compile(r'^\d+')
    search_result = expr.search(v)

    if not search_result:
        return False
    _, end_n = search_result.span()
    value = int(v[:end_n])
    unit = v[end_n:]

    if unit == 'cm':
        return 150 <= value <= 193
    if unit == 'in':
        return 59 <= value <= 76

    return False


required_fields = [
    ('byr', lambda v: len(v) == 4 and (1920 <= int(v) <= 2002)),
    ('iyr', lambda v: len(v) == 4 and (2010 <= int(v) <= 2020)),
    ('eyr', lambda v: len(v) == 4 and (2020 <= int(v) <= 2030)),
    ('hgt', validate_height),
    ('hcl', lambda v: re.compile(r'^#([0-9]|[a-f]){6}$').search(v)),
    ('ecl', lambda v: re.compile(
        r'^(amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)$').search(v)),
    ('pid', lambda v: re.compile(r'^\d{9}$').search(v)),


    # 'cid'
]

with open('input/4.txt') as f:
    text_input = f.read()
    passports = get_passports(text_input)

    n_valid = sum([is_passport_valid(p, required_fields) for p in passports])
    print('n_valid:', n_valid)
