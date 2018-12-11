#!/usr/bin/python

import fileinput
from collections import deque
from collections import namedtuple
from itertools import product

PointVector = namedtuple('PointVector', 'x y dx dy')

def get_input():
    for line in fileinput.input():
        i = line.find(' v')
        position, velocity = line[:i-1], line[i+1:-2]
        x, y = map(int, position.lstrip('position=<').split(','))
        dx, dy = map(int, velocity.lstrip('velocity=<').split(','))
        yield PointVector(x+dx, y+dy, dx, dy)

def height(points):
    y_values = [p.y for p in points]
    return max(y_values) - min(y_values) + 1

def timewarp(vectors, step=1):
    if step == 0:
        return
    for i in range(len(vectors)):
        v = vectors[-1]
        vectors[-1] = PointVector(v.x+(step*v.dx), v.y+(step*v.dy), v.dx, v.dy)
        vectors.rotate(1)

def has_neighbors(point, coords):
    x, y = point
    square = ((-1,  1), ( 0,  1), ( 1,  1),
              (-1,  0),           ( 1,  0),
              (-1, -1), ( 0, -1), ( 1, -1))
    for dx, dy in square:
        if (dx, dy) == (0, 0):
            continue
        elif (x+dx, y+dy) in coords:
            return True
    return False

def display(vectors):
    x_values = [v.x for v in vectors]
    y_values = [v.y for v in vectors]
    coords = zip(x_values, y_values)
    for y in range(min(y_values), max(y_values)+1):
        for x in range(min(x_values), max(x_values)+1):
            if (x, y) in coords:
                print '#',
            else:
                print ' ',
        print

def solve():
    vectors = deque([v for v in get_input()])
    last_height = height(vectors)
    seconds = 0
    jump = (last_height / 10) + 1
    while True:
        seconds += jump
        timewarp(vectors, jump)
        curr_height = height(vectors)
        if curr_height > last_height:
            jump = -jump/2 or 2
        elif curr_height <= 20:
            coords = [(vector.x, vector.y) for vector in vectors]
            if all(has_neighbors(point, coords) for point in coords):
                return vectors, seconds+1
        last_height = curr_height

def main():
    part1, part2 = solve()
    print 'Part 1: I found a message!'
    display(part1)
    print 'Part 2:', part2

if __name__ == '__main__':
    main()
