#!/usr/bin/python

def react(j, k):
    combo = j + k
    if combo.isupper() or combo.islower():
        return False
    elif j.lower() == k.lower():
        return True
    else:
        return False
    
def main():
    with open('input', 'rb') as infile:
        units = ['']
        for k in iter(lambda: str(infile.read(1)), b''):
            if not k.strip():
                continue
            j = units[-1]
            if react(j, k):
                units.pop()
            else:
                units.append(k)
    del(units[0])
    
    results = {}
    for unit in map(chr, range(ord('a'), ord('z')+1)):
        data = ''.join(units).translate(None, unit.upper()+unit.lower())
        testunits = ['']
        for k in data:
            j = testunits[-1]
            if react(j, k):
                testunits.pop()
            else:
                testunits.append(k)
        del(testunits[0])
        results[unit.lower()] = len(testunits)
    problem = min(results.keys(), key=results.get)

    return len(units), results[problem]

if __name__ == '__main__':
    answers = main()
    print 'Part 1:', answers[0]
    print 'Part 2:', answers[1]
