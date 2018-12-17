#!/usr/bin/pypy

import sys

class scores(object):
    def __init__(self):
        self.elves = [0, 1]
        self.scoreboard = list([3,7])

    def tally(self):
        score = self.scoreboard[self.elves[0]]
        score += self.scoreboard[self.elves[1]]
        self.scoreboard.extend(divmod(score, 10) if score > 9 else (score,))
        n = len(self)
        self.elves[0] = (self.elves[0] + self[self.elves[0]] + 1) % n
        self.elves[1] = (self.elves[1] + self[self.elves[1]] + 1) % n

    def __getitem__(self, index):
        return self.scoreboard[index]

    def __len__(self):
        return len(self.scoreboard)

def main():
    try:
        puzzle = int(sys.argv[1])
        puzzle2 = sys.argv[1]
    except:
        print 'usage: {} <puzzle-input>'.format(sys.argv[0])
        sys.exit(1)

    scoreboard = scores()
    while len(scoreboard) < puzzle + 10:
        scoreboard.tally()
    print 'Part 1:', ''.join(map(str, scoreboard[puzzle:puzzle+10]))

    matched = False
    i = 0
    while not matched:
        for n in range(10000):
            scoreboard.tally()
        i += 10000
        chunk = ''.join(map(str, scoreboard[i-10000:i]))
        if puzzle2 in chunk:
            matched = True
            n = chunk.find(puzzle2)
            print 'Part 2:', n+i-10000


if __name__ == '__main__':
    main()
