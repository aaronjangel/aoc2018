#!/usr/bin/python

with open('input') as infile:
    lines = infile.readlines()

two = 0
three = 0
for line in lines:
    freqs = {}
    for letter in line:
        freqs[letter] = freqs.get(letter, 0) + 1
    for letter in line:
        if freqs[letter] == 2:
            two += 1
            break
    for letter in line:
        if freqs[letter] == 3:
            three += 1
            break
part1 = two * three

similar = []
for i in range(len(lines)):
    line1 = lines[i].rstrip()
    for line2 in lines[i:]:
        diff = 0
        line2 = line2.rstrip()
        for j in range(len(line1)):
            if line1[j] != line2[j]:
                diff += 1
        if diff == 1:
            similar.append((line1, line2))

answer = []
for line1, line2 in similar:
    for i in range(len(line1)):
        if line1[i] == line2[i]:
            answer.append(line1[i])
part2 = ''.join(answer)

print 'Part 1:', part1
print 'Part 2:', part2
