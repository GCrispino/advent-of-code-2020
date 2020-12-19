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
    Xs = []
    for i, (m, b) in enumerate(zip(mask[2:], padded_bin_val[2:])):
        if m == '0':
            new_padded_bin_val.append(b)
        elif m == '1':
            new_padded_bin_val.append('1')
        else:
            new_padded_bin_val.append('X')
            Xs.append(i)
    addresses = []

    n_X = len(Xs)
    bin_n_X = bin(2 ** (n_X - 1))
    for i_b in range(2 ** n_X):
        b = bin(i_b)
        padded_b = pad_bin(b, size=len(bin_n_X) - 2)

        addr = new_padded_bin_val[:]
        for k, b_d in enumerate(padded_b[2:]):
            addr[Xs[k] + 2] = b_d
        addresses.append(addr)
        addresses[-1] = ''.join(addresses[-1])

    return addresses


with open('input/14.txt') as f:
    lines = f.readlines()
    program = parse_program(lines)
    addresses = {}
    cur_mask = None
    for addr, ins in program:
        if addr is None:
            cur_mask = '0b' + ins
        else:
            for addr_ in apply_mask(addr, cur_mask):
                addresses[int(addr_, base=2)] = ins
    res = sum(addresses.values())
    print(res)
