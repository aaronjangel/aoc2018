#!/usr/bin/python

part1 = 0
with open('input') as infile:
    part1 = sum(int(line) for line in infile)
    infile.seek(0)
    freq = 0
    seen = {0: 1}
    while seen[freq] < 2:
        for line in infile:
            freq += int(line)
            seen[freq] = seen.get(freq, 0) + 1
            if seen[freq] > 1:
                break
        infile.seek(0)
    part2 = freq

print 'Part 1:', part1
print 'Part 2:', part2
