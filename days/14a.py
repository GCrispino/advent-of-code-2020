import re


def parse_program(lines):

    program = []
    for ins in lines:
        spl = ins.split(' = ')
        match = re.search(r'\[\d+\]', spl[0])
        if not match:
            # mask
            maddress = None
            val = spl[1].strip()
        else:
            # not mask
            span = match.span()
            # print(spl[0], span)
            maddress = int(ins[span[0] + 1:span[1] - 1])
            val = int(spl[1])
        program.append((maddress, val))

    return program


def pad_bin(bin_val, size=36):
    payload = bin_val.split('0b')[1]
    length = len(payload)
    return '0b' + ('0' * (size - length)) + payload


def apply_mask(val, mask):
    bin_val = bin(val)
    padded_bin_val = pad_bin(bin_val)
    new_padded_bin_val = ['0', 'b']
    for m, b in zip(mask, padded_bin_val[2:]):
        if m == 'X':
            new_padded_bin_val.append(b)
            continue
        new_padded_bin_val.append(m)

    return int(''.join(new_padded_bin_val), base=2)


with open('input/14.txt') as f:
    lines = f.readlines()
    program = parse_program(lines)
    addresses = {}
    cur_mask = None
    for addr, ins in program:
        if addr is None:
            cur_mask = ins
        else:
            addresses[addr] = apply_mask(ins, cur_mask)
    print(addresses)
    res = sum(addresses.values())
    print(res)
