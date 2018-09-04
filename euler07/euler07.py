# PE 7
# What is the 10001 prime number

import sys
import random
import math

primes = [2,3,5,7,11,13]

for x in range(14,105000):
    for y in range(int(math.sqrt(x)+1),1,-1):
        if(x % y == 0):
            x=x+1
            break

        elif((x % y != 0) and (y==2)):
            primes.append(x)
            x=x+1
            continue


print(str(primes[10000]) + " is the 10001 prime")
