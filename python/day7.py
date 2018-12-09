#!/usr/bin/python

from copy import deepcopy

steps = []
root = {}

with open('input') as infile:
    for line in infile.readlines():
        _, dep, _, _, _, _, _, step, _, _ = line.split()
        if step not in steps:
            steps.append(step)
        if dep not in steps:
            steps.append(dep)
        if step not in root:
            root[step] = []
        root[step].append(dep)

def nextsteps(steps, tree, completed):
    scratch = tree.keys() + completed
    return sorted([step for step in steps if step not in scratch])

def part1(steps, tree):
    order = nextsteps(steps, tree, [])[0]
    candidates = []
    while len(tree) > 0:
        completed = list(order)
        for step, deps in tree.items():
            for dep in deps:
                if dep in completed:
                    deps.remove(dep)
            if not deps:
                candidates.append(step)
                del tree[step]
        order += nextsteps(steps, tree, completed)[0]
    return order

def part2(steps, order, tree, workers, delay):
    def steptime(step):
        return delay + ord(step) - ord('A') + 1

    def load(queues, tasks):
        loaded = []
        for i, queue in queues.items():
            if (not len(queue)) and tasks:
                step = tasks[0]
                queue += [step] * steptime(step)
                loaded += step
                del(tasks[0])
        return loaded

    def timewarp(queues, interval):
        completed = []
        for i, queue in queues.items():
            if queue and len(queue) <= interval:
                completed += queue[0]
            del(queue[:interval])
        return completed

    def prune(tree, dead):
        for branch in dead:
            for trunk, branches in tree.items():
                if branch in branches:
                    tree[trunk].remove(branch)
                if not len(tree[trunk]):
                    del(tree[trunk])

    ready = []
    completed = []
    queued = []
    elapsed = 0
    queues = {n: [] for n in range(workers)}
    while len(completed) < len(steps):
        capacity = len([q for q in queues if len(queues[q]) == 0])
        candidates = nextsteps(steps, tree, completed)
        scratch = []
        for step in list(candidates):
            if step in completed:
                candidates.remove(step)
                scratch.append(step)
            elif step in queued:
                candidates.remove(step)
                scratch.append(step)
        ready += [step for step in candidates][:capacity-len(ready)]
        work = load(queues, ready)
        queued += work
        interval = min([len(queues[q]) for q in queues if len(queues[q])])
        work = timewarp(queues, interval)
        map(queued.remove, work)
        completed = list(set(completed+work))
        prune(tree, dead=completed)
        elapsed += interval
    return elapsed

answer1 = part1(steps, deepcopy(root))
answer2 = part2(steps, answer1, deepcopy(root), 6, 60)
print 'Part 1:', answer1
print 'Part 2:', answer2
