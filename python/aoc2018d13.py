#!/usr/bin/pypy

from collections import Counter, defaultdict
from itertools import count
import fileinput
import sys


class Cart(object):
    def __init__(self, position, direction):
        if isinstance(position, tuple):
            x, y = position
            p = x-y*1j
        elif isinstance(position, complex):
            p = position
        else:
            raise ValueError('position must be tuple or complex')
        self._position = p

        if isinstance(direction, basestring):
            if len(direction) > 1:
                raise Valueerror('too many directional characters')
            d = {'^': 1j**1, '<': 1j**2, 'v': 1j**3, '>': 1j**4}[direction]
        elif isinstance(direction, tuple):
            x, y = direction
            d = x-y*1j
        elif isinstance(direction, complex):
            d = direction
        else:
            raise ValueError('diection must be string, tuple, or complex')
        self._direction = d

        self._intersections = 0
        self._crashed = False

    def move(self, tracks):
        if self.crashed:
            return
        self._position += self._direction
        t = tracks.get(self._position, None)
        if t == '+':
            self._direction *= [1j, 1, -1j][self._intersections%3]
            self._intersections += 1
        elif t == '/':
            if self._direction in (1, -1):
                self._direction *= 1j
            else:
                self._direction *= -1j
        elif t == '\\':
            if self._direction in (1j, -1j):
                self._direction *= 1j
            else:
                self._direction *= -1j

    def crash(self):
        self._crashed = True

    @property
    def crashed(self):
        return self._crashed

    @property
    def picture(self):
        if self.crashed:
            return 'X'
        else:
            return {1j: '^', -1: '<', -1j: 'v', 1: '>'}[self._direction]

    @property
    def position(self):
        return self._position

    @property
    def direction(self):
        return self._direction

    @property
    def point(self):
        x, y = map(int, (self._position.real, -self._position.imag))
        return x, y

def print_map(carts, tracks, crashes=True):
    return
    trackmap = tracks.copy()
    if crashes:
        trackmap.update({cart.position: cart.picture for cart in carts})
    else:
        trackmap.update({cart.position: cart.picture for cart in carts if not cart.crashed})
    points = trackmap.keys()
    x = map(int, (p.real for p in points))
    y = map(int, (-p.imag for p in points))
    maxx, maxy = max(x), max(y)
    for y in range(maxy+1):
        track = []
        for x in range(maxx+1):
            p = x-y*1j
            if p in trackmap:
                track.append(trackmap[p])
            else:
                track.append(' '),
        print ''.join(track)

def parse_input(infile):
    carts = []
    tracks = {}
    for y, line in enumerate(infile):
        for x, char in enumerate(line.rstrip()):
            p = x-y*1j
            if char in ('^', '<', 'v', '>'):
                carts.append(Cart(p, char))
                tracks[p] = {'^': '|', '<': '-', 'v': '|', '>': '-'}[char]
            else:
                tracks[p] = char
    return carts, tracks

def crash(carts, tracks):
    crashes = []
    carts.sort(key=lambda c: reversed(c.point))
    for cart in carts:
        if cart.crashed:
            continue
        cart.move(tracks)
        for cart2 in carts:
            if cart2.crashed or cart == cart2:
                continue 
            if cart.position == cart2.position:
                cart.crash()
                crashes.append(cart)
                cart2.crash()
                crashes.append(cart2)
    if crashes:
        return crashes

def main():
    if len(sys.argv) < 2:
        print 'Reading input from stdin.'
    carts, tracks = parse_input(fileinput.input())
    crashes = []
    while not crashes:
        crashes = crash(carts, tracks)
    print_map(carts, tracks, crashes=True)
    x, y = crashes[0].point
    print 'Part 1:', '{},{}'.format(x, y)
    while len(crashes) < len(carts) - 1:
        last_crashes = crash(carts, tracks)
        if last_crashes:
            crashes += last_crashes
        print_map(carts, tracks, crashes=True)
    uncrashed = [cart for cart in carts if not cart.crashed]
    x, y = uncrashed[0].point
    print 'Part 2:', '{},{}'.format(x, y)

if __name__ == '__main__':
    main()

