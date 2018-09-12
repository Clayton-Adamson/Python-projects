"""
PE 49:

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways:
(i) each of the three terms are prime, and,
(ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property,
 but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?
"""

import math
from itertools import permutations

# this one took a while, but it was worth it!
# This code isn't the prettiest, BUT IT'S SO FAST!!!!!!!

full_primes = [2]

for x in range(3,9999):

    for y in full_primes:

        if(x % y == 0):
            break

        elif(y>math.sqrt(x)):
            full_primes.append(x)
            break

primes = []

# removes primes < 1000
for x in full_primes:
    if(x>1000):
        primes.append(x)


# Generates a list of all permutations of a number in a given list
def generate_perm(num, target):

    temp_list = [int(''.join(i)) for i in sorted(list(permutations(str(num))))]

    '''
    I want to remove all permutations less than 4 digits (happens when int has a leading 0)
    Making a copy of the list and removing elements from that DID NOT work...
    idk why... if i'm not touching the list in charge of iterative bounds (temp_list)... shouldn't it work?
    O well.. at least I can append to a new list, but i feel like this wastes time.
    On the plus side, by appending, I can put in a second condition to stop repeat permutations
    '''
    perm_list = []

    for x in temp_list:
        if(x in target and x not in perm_list):
            perm_list.append(x)

    return perm_list

# checks if primes in a list have an arithmetic property and returns concatenated answer
def add_sequence(prime_list):

    length = len(prime_list)

    if(length < 3):
        return 0

    else:
        sub_list = []
        for x in prime_list:
            for y in prime_list:
                if(y >= x):
                    break

                else:
                    diff = x-y
                    for a in range(0,length-2):
                        if(prime_list[a] + diff == prime_list[a+1] and prime_list[a+1] + diff == prime_list[a+2]):
                            return "".join(str(prime_list[a]) + str(prime_list[a+1]) + str(prime_list[a+2]))

    return 0


for x in primes:

    answer = add_sequence(generate_perm(x,primes))

    if(answer != 0):
        print(answer)
        break
