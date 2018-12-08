#!/usr/bin/python

def mdist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def mclosest(p, points):
    r = {}
    for q in points:
        d = mdist(p, q)
        if d in r:
            r[d].append(q)
        else:
            r[d] = [q]
    d = min(r)
    if len(r[d]) != 1:
        return None
    else:
        return r[d][0]

def main():
    maxx, maxy = (0, 0)
    points = []
    labels = {}
    n = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx'
    i = 0
    with open('input') as input:
        for coord in input.readlines():
            x, y = map(int, coord.split(','))
            if x > maxx:
                maxx = x
            if y > maxy:
                maxy = y
            points.append((x, y))
            labels[(x, y)] = n[i]
            i += 1
    part1 = {p: [p] for p in points}
    part2 = []
    for y in range(0, maxy+1):
        for x in range(0, maxx+1):
            p = x, y
            if p not in points:
                q = mclosest(p, points)
                if not q:
                    pass
                if x in (0, maxx) or y in (0, maxy):
                    part1[q] = []
                elif part1[q]:
                    part1[q].append(p)
            if sum(mdist(p, q) for q in points) < 10000:
                part2.append(p)
    d = 0
    p = None
    for q in part1.keys():
        if len(part1[q]) > d:
            d = len(part1[q])
            p = q
    print 'Part 1:', d
    print 'Part 2:', len(part2)

if __name__ == '__main__':
    main()
