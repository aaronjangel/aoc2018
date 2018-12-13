#!/usr/bin/pypy

from collections import defaultdict
import sys


def part1(plants, rules, generations=20):
    print
    s = ''.join('#' if n in plants else '.' for n in range(min(plants)-4, min(plants)-4+130)), sum(plants)
    print ' 0', s
    for i in range(generations):
        minp = min(plants) - 4
        maxp = max(plants) + 4
        s = ''.join(['#' if n in plants else '.' for n in range(minp, maxp)])
        plants = []
        for n in range(2, maxp+8):
            p = s[n-2:n+3]
            if rules[p] == '#':
                plants.append(n+minp)
        s2 = ''.join('#' if n in plants else '.' for n in range(minp, minp+130)), sum(plants)
        print str(i+1).rjust(2), s2
    print '  ', ''.join('^' if n == 0 else ' ' for n in range(minp, minp+130)), sum(plants)
    return sum(plants)

def main():
    try:
        infile = sys.argv[1]
        gens = int(sys.argv[2])
    except:
        print 'usage: {} <input-file> <generations>'.format(sys.argv[0])
        sys.exit(1)

    rules = defaultdict(lambda: '.')
    with open(infile) as data:
        for line in data.readlines():
            if line.startswith('initial'):
                s = line.split(':')[1].strip()
                plants = [i for i in range(len(s)) if s[i] == '#']
            elif '=>' in line:
                pattern, result = line.strip().split(' => ')
                rules[pattern] = result

    print 'Part 1:', part1(plants, rules, gens)
    #print 'Part 2:', part2()

if __name__ == '__main__':
    main()
