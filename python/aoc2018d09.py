#!/usr/bin/python

from collections import deque

def solve(nplayers, lastmarble):
    score = 0
    scores = {n: 0 for n in range(nplayers)}
    player = 0
    marbles = deque([0])
    turns = 0
    
    while turns < lastmarble:
        turns += 1
        if turns > 0 and turns % 23 == 0:
            scores[player] += turns
            marbles.rotate(-7)
            scores[player] += marbles.pop()
        else:
            marbles.rotate(2) # at ~1 am, this made perfect sense; but after
                              # having slept, it took me a minute to figure
                              # out *how* it worked when took a second look.
            marbles.append(turns)
        player += 1 if player < nplayers-1 else -player
    return max(scores.values())

with open('input') as infile:
    line = infile.readline()

nplayers = int(line.split()[0])
lastmarble = int(line.split()[6])

part1 = solve(nplayers, lastmarble)
print 'Part 1: ', part1

part2 = solve(nplayers, lastmarble*100)
print 'Part 2: ', part2
