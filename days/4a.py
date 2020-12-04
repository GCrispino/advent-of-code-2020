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
    return all([f in passport for f in required_fields])


required_fields = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    # 'cid'
]

with open('input/4.txt') as f:
    text_input = f.read()
    passports = get_passports(text_input)

    n_valid = sum([is_passport_valid(p, required_fields) for p in passports])
    print('n_valid:', n_valid)
