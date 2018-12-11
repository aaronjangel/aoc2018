#!/usr/bin/pypy

from functools import wraps

def memoize(f):
    memo = {}

    @wraps(f)
    def wrapper(*args):
        try:
            return memo[args]
        except KeyError:
            rv = f(*args)
            memo[args] = rv
            return rv
    return wrapper

@memoize
def hpowerlevel(x, y, s, h):
    """Calculate the power level of a column of cells.

    args:
        x (int): left-most cell identifier
        y (int): right-most cell identifier
        s (int): serial number
        h (int): height of the column

    returns:
        the total power level for all cells in the column identified
        by the arguments.
    """
    np = 0
    points = ((x, y) for y in range(y, y+h))
    for p in points:
        x, y = p
        np += powerlevel(x, y, s, 1)
    return np

@memoize
def powerlevel(x, y, s, n):
    """Calculate the power level of a square of cells.

    args:
        x (int): left-most cell identifier
        y (int): upper-most cell identifier
        s (int): serial number
        n (int): size of the square

    returns:
        the total power level for all cells in the square identified
        by the arguments.
    """
    np = 0
    if n > 1:
        for x in range(x, x+n):
            np += hpowerlevel(x, y, s, n)
    else:
        for y in range(y, y+n):
            rp = 0
            for x in range(x, x+n):
                r = x + 10
                p = r * y
                p += s
                p *= r
                p = (p // 100) % 10
                p -= 5
                rp += p
            np += rp
    return np

def maxpower(s, n, maxx=300, maxy=300):
    p = {(x, y): powerlevel(x, y, s, n)
            for x in range(1, maxx+1) for y in range(1, maxy+1)
            if x-1 <= maxx-n and y-1 <= maxy-n}
    x, y = max(p, key=p.get)
    return x, y, p[x, y]

def part1(s):
    x, y, l = maxpower(s, 3)
    return '{},{}'.format(x, y)

def part2(s):
    p = {}
    ll = 0
    for n in range(1, 301):
        x, y, l = maxpower(s, n)
        p[x, y, n] = l
        # If we drop off too fast, give up, because we've peaked. 
        if l < ll-10:
            break
        else:
            ll = l
    x, y, n = max(p, key=p.get)
    return '{},{},{}'.format(x, y, n)

def main():
    with open('input') as infile:
        s = int(infile.readline())
    print 'Part 1:', part1(s)
    print 'Part 2:', part2(s)

if __name__ == '__main__':
    main()

