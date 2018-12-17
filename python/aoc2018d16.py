#!/usr/bin/pypy

from collections import defaultdict


class Machine(object):
    def __init__(self, r1=0, r2=0, r3=0, r4=0, opcodes=[], instructions=[]):
        self._registers = [r1, r2, r3, r4]
        self._opcodes = opcodes
        self._instructions = instructions

    def __call__(self):
        for opcode, a, b, c in self._instructions:
            if opcode not in self._opcodes:
                raise ValueError('opcode {} not defined'.format(opcode))
            op = getattr(self, self._opcodes[opcode])
            op(a, b, c)

    @property
    def mnemonics(self):
        return ['addr', 'addi', 'mulr', 'muli',
                'banr', 'bani', 'borr', 'bori',
                'setr', 'seti',
                'gtir', 'gtri', 'gtrr',
                'eqir', 'eqri', 'eqrr']

    def rafunc(self, func, a, b, c):
        func(self._registers[a], b, c)

    def rbfunc(self, func, a, b, c):
        func(a, self._registers[b], c)

    def addi(self, a, b, c):
        self._registers[c] = self._registers[a] + b

    def addr(self, *args):
        self.rbfunc(self.addi, *args)

    def muli(self, a, b, c):
        self._registers[c] = self._registers[a] * b

    def mulr(self, *args):
        self.rbfunc(self.muli, *args)

    def bani(self, a, b, c):
        self._registers[c] = self._registers[a] & b

    def banr(self, *args):
        self.rbfunc(self.bani, *args)

    def bori(self, a, b, c):
        self._registers[c] = self._registers[a] | b

    def borr(self, *args):
        self.rbfunc(self.bori, *args)

    def seti(self, a, b, c):
        self._registers[c] = a

    def setr(self, *args):
        self.rafunc(self.seti, *args)

    def gtir(self, a, b, c):
        self._registers[c] = 1 if a > self._registers[b] else 0

    def gtri(self, a, b, c):
        self._registers[c] = 1 if self._registers[a] > b else 0

    def gtrr(self, *args):
        self.rafunc(self.gtir, *args)

    def eqir(self, a, b, c):
        self._registers[c] = 1 if a == self._registers[b] else 0

    def eqri(self, a, b, c):
        self._registers[c] = 1 if self._registers[a] == b else 0

    def eqrr(self, *args):
        self.rafunc(self.eqir, *args)


def testall(before, values, after):
    r = []
    m = Machine()
    funcs = m.mnemonics
    for f in funcs:
        m._registers = list(before)
        func = getattr(m, f)
        func(*values)
        if m._registers == after:
            r.append(f)
    return r

def main():
    r = 0
    before, values, after = [], [], []
    opcodes = defaultdict(list)
    m = Machine()
    instructions = []
    with open('input') as infile:
        for line in infile.readlines():
            if not line.strip():
                before, values, after = [], [], []
            else:
                if line.startswith('B'):
                    before = map(int, line[9:-2].split(','))
                elif line.startswith('A'):
                    after = map(int, line[9:-2].split(','))
                    possible = testall(before, values[1:], after)
                    r += 1 if len(possible) >= 3 else 0
                    opcodes[values[0]].append(possible)
                else:
                    values = map(int, line.strip().split(' '))
                    if not before:
                        instructions.append(values)
    print 'Part 1:', r
    opcodes = {opcode: set.intersection(*map(set, possibles))
        for opcode, possibles in opcodes.items()}
    new_opcodes = {}
    while len(new_opcodes) < len(opcodes):
        for opcode, possibles in opcodes.items():
            plist = list(possibles)
            if len(possibles) == 1 and plist[0] not in new_opcodes.values():
                mnemonic = plist[0]
                new_opcodes[opcode] = mnemonic
                print 'opcode {} maps to {}'.format(str(opcode).rjust(2), mnemonic)
                for opcode in opcodes:
                    opcodes[opcode].discard(mnemonic)

    m = Machine(opcodes=new_opcodes, instructions=instructions)
    m()
    print 'Part 2:', m._registers[0]


if __name__ == '__main__':
    main()
