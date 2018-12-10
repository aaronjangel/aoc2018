#!/usr/bin/python

with open('input') as infile:
    lines = sorted(infile.readlines())

guards = {}
guard = None
sleepmin = None

sleepy = '3209'
sleepyt = {}
sleepy2 = {}

for line in lines:
    line = line.lstrip('[').rstrip()
    ts, desc = line.split('] ')
    if desc.endswith('begins shift'):
        guard = desc.lstrip('Guard #').rstrip(' begins shift')
    else:
        dt, tm = ts.split(' ')
        hour, minute = map(int, tm.split(':'))
        if desc == 'wakes up':
            guards[guard] = guards.get(guard, 0) + minute - sleepmin
            for m in range(minute - sleepmin):
                key = ':'.join((guard, str(m+sleepmin)))
                sleepy2[key] = sleepy2.get(key, 0) + 1
                if guard == sleepy: 
                    sleepyt[m+sleepmin] = sleepyt.get(m+sleepmin, 0) + 1
        if desc == 'falls asleep':
            sleepmin = minute

# Part I
guard = int(max(guards.keys(), key=guards.get))
minute = max(sleepyt.keys(), key=sleepyt.get)
print 'Part 1:', guard*minute

# Part II
guard, minute = map(int, max(sleepy2.keys(), key=sleepy2.get).split(':'))
print 'Part 2:', guard*minute
