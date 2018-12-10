#!/usr/bin/python
#
# Here is a (sloppier) version of a Python solution to day 9 that doesn't
# import any extra modules. It's also quite a bit slower, but it still
# completes in under a minute.
#
# This was fun, because I have never had to occasion to use, let alone
# write, anything to solve this type of problem.
#

class CircularList(object):
    def __init__(self, values=[]):
        self._cursor = self
        self._before = self
        self._after = self
        self._value = values.pop(0)
        for value in values:
            self.append(value)
        values.insert(0, self._value)

    def append(self, value):
        appendage = CircularList([value])
        appendage._before = self._cursor
        appendage._after = self._cursor._after
        self._cursor._after._before = appendage
        self._cursor._after = appendage
        self._cursor = appendage

    def pop(self):
        popped_value = self._cursor._value
        self._cursor._before._after = self._cursor._after
        self._cursor._after._before = self._cursor._before
        self._cursor = self._cursor._before
        return popped_value

    def rotate(self, n):
        for i in range(n) if n >= 0 else range(n, 0):
            if n >= 0:
                self._cursor = self._cursor._after
            else:
                self._cursor = self._cursor._before

    def __repr__(self):
        r = repr(self._value)
        cursor = self._after
        while cursor != self:
            if cursor == self._cursor:
                r += ',* '
            else:
                r += ',  '
            r += (repr(cursor._value))
            cursor = cursor._after
        return '{}({})'.format(self.__class__.__name__, r)


def solve(nplayers, lastmarble):
    score = 0
    scores = {n: 0 for n in range(nplayers)}
    player = 0
    marbles = CircularList([0])
    turns = 0
    
    while turns <= lastmarble:
        turns += 1
        if turns > 0 and turns % 23 == 0:
            scores[player] += turns
            marbles.rotate(-7)
            scores[player] += marbles.pop()
            marbles.rotate(1)
        else:
            marbles.rotate(1)
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
