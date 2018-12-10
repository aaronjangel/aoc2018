#!/usr/bin/python

def data2():
    with open('input') as input:
        buf = ''
        for c in iter(lambda: str(input.read(1)), b''):
            if c == ' ':
                yield int(buf)
                buf = ''
            else:
                buf += c

with open('input') as input:
    line = input.readline().strip()

data = map(int, line.split())

def metasum(node):
    n_children = node.pop(0)
    n_metadata = node.pop(0)
    metadata = 0

    while n_children:
        metadata += metasum(node)
        n_children -= 1

    while n_metadata:
        metadata += node.pop(0)
        n_metadata -= 1

    return metadata

def nodevalue(node):
    n_children = node.pop(0)
    n_metadata = node.pop(0)
    children = []
    value = 0

    while n_children:
        children.append(nodevalue(node))
        n_children -= 1

    while n_metadata:
        metadata = node.pop(0)
        n_metadata -= 1
        if not children:
            value += metadata
        elif children and metadata <= len(children):
            value += children[metadata-1]

    return value

print 'Part 1:', metasum(list(data))
print 'Part 2:', nodevalue(list(data))
