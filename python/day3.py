#!/usr/bin/python

import pickle

squares = {}
with open('input') as input:
    for line in input:
        sid, spec = line.rstrip().split(' @ ')
        loc, size = spec.split(': ')
        x, y = map(int, loc.split(','))
        w, h = map(int, size.split('x'))
        for i in range(w):
            for j in range(h):
                if i+x not in squares:
                   squares[i+x] = {}
                if j+y not in squares[i+x]:
                   squares[i+x][j+y] = 0
                squares[i+x][j+y] += 1

part1 = 0
for x, row in squares.items():
    for y, square in squares[x].items():
        if square > 1:
            part1 += 1

with open('input') as input:
    for line in input:
        sid, spec = line.rstrip().split(' @ ')
        loc, size = spec.split(': ')
        x, y = map(int, loc.split(','))
        w, h = map(int, size.split('x'))
        overlap = False
        for i in range(w):
            for j in range(h):
                if squares[i+x][j+y] > 1:
                    overlap = True
        if not overlap:
            break
part2 = int(line.split(' ')[0].lstrip('#'))

print 'Part 1:', part1
print 'Part 2:', part2
