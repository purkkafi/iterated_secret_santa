#!/usr/bin/python3

from collections import Counter as multiset
from itertools import combinations as subsets
import csv, sys, random

# By MathOverflow user smichr
# https://mathoverflow.net/a/351024
def derangements(S):
    """Yield unique derangements of S which is comprised of hashable
    elements.

    Examples
    ========

    >>> [''.join(i) for i in derangements('abbcc')]
    ['bccba', 'bccab', 'cacbb', 'ccabb']

    The return value is a list of elements of S which is modified
    internally in place, so a copy of the return value should be
    made if collecting the results in a list (or strings should be
    joined as shown above):

    >>> [i for i in derangements([1,2,3,3])]
    [[3, 3, 2, 1], [3, 3, 2, 1]]
    >>> [i.copy() for i in derangements([1,2,3,3])]
    [[3, 3, 1, 2], [3, 3, 2, 1]]

    """
  # S must contain hashable elements
    s = set(S)
  # at each position, these are what may be used
    P = [sorted(s - set([k])) for k in S]
  # these are the counts of each element
    C = multiset(S)
  # the index to what we are using at each position
    I = [0]*len(P)
  # the list of return values that will be modified in place
    rv = [None]*len(P)
  # we know the value that occurs most will be located in subsets
  # of the other positions so find those positions...
    mx = max(C.values())
    for M in sorted(C):
        if C[M] == mx:
            break
    ix = [i for i,c in enumerate(S) if c != M]
  # remove M from its current locations...
    for i in ix:
        P[i].remove(M)
  # and make them fixed points each time.
    for fix in subsets(ix, mx):
        p = P.copy()
        for i in fix:
            p[i] = [M]
        while 1:
            Ci = C.copy()
            for k, pk in enumerate(p):
                c = pk[I[k]]
                if Ci[c] == 0:
                  # can't select this at position k
                    break
                else:
                    Ci[c] -= 1
                    rv[k] = c
            else:
                yield(rv)
          # increment last valid index
            I[k] = (I[k] + 1)%len(p[k])
            if I[k] == 0:
              # set all to the right back to 0
                I[k + 1:] = [0]*(len(I) - k - 1)
              # carry to the left
                while k and I[k] == 0:
                    k -= 1
                    I[k] = (I[k] + 1)%len(p[k])
            if k == 0 and I[k] == 0:
                break

if len(sys.argv) != 3:
    print('Arguments: [gift_data] [present]')
    print('[gift_data]: .csv file with gift data (see example)')
    print('[present]: comma-separated list of people present for this round')
    exit()

# Gifts from giver to reciever as times given
# gifts[giver][reciever] = (times given)
gifts = {}

# Names of givers and recievers
names = []

# Read gift data from csv
with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile)
    
    # Read names form initial line, skipping the empty first value
    names = [s.strip() for s in reader.__next__()[1:]]
    
    for i, row in enumerate(reader):
        giver = row[0].strip()
        
        if giver != names[i]:
            raise ValueError(f"names don't match in row and column: {giver}, {names[i]}")
        
        gifts[giver] = {}
        
        for a, times in enumerate(row[1:]):
            reciever = names[a]
            times = times.strip()
            
            if giver == reciever: # Ignore cells where giver = reciever
                continue
            
            if times == '': # Special case: empty cells count as 0
                times = 0
            
            gifts[giver][reciever] = int(times)

# List of who is present from argument
present = sys.argv[2].split(',')

# Generate list of people not present
not_present = list(names)
for p in present:
    if p not in gifts.keys():
        raise ValueError(f'{p} not listed in csv')
    not_present.remove(p)

# Remove unneeded data about people not present
for np in not_present:
    del gifts[np] # gifts from people not present

for p in present:
    for np in not_present:
        del gifts[p][np] # gifts to people not present

# Returns the value of a derangement where present[n] is giving a gift to dr[n]
# Lower is better
def dr_value(dr):
    acc = 0
    
    for i, giver in enumerate(present):
        
        # Assuming gifts are given as specified by the argument, finds the
        # highest value in every row and increases the accumulator by it
        highest = -1
        for reciever in present:
            if giver == reciever:
                continue
            
            if dr[i] == reciever:
                val = gifts[giver][reciever] + 1 # gift will be given on this round
            else:
                val = gifts[giver][reciever] # normal value listed in .csv
            
            if val > highest:
                highest = val
        
        acc = acc + highest
    
    return acc

# Iterate over all derangements
lowest_val = 1000000000000000 # placeholder large value
good_drs = [] # holds best possible derangements found so far

for i,d in enumerate(derangements(present)):

    # Print progress for large enumerations
    if i > 0 and i % 1000 == 0:
        print(f'Checking {i}/?, possible results found: {len(good_drs)}')
        
    val = dr_value(d)
    
    if val > lowest_val:
        continue
    elif val == lowest_val: # Add current derangement to the list
        good_drs.append(list(d)) # Copy the list, see derangements(S)
    else:
        good_drs = [] # Reset list because the new lowest_val is lower
        good_drs.append(list(d)) # Copy the list, see derangements(S)
        lowest_val = val

# Choose one of the best ones
chosen = random.choice(good_drs)

# Write results to stdout
result = []
for i in range(0, len(present)):
    result.append(f'{present[i]} -> {chosen[i]}')
result = '\n'.join(result)

print(result)
