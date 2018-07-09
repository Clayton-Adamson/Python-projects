# PE 1
# Find the sum of all multiples of 3 or 5 below 1000

import sys
import random
import math


sum = 0
for x in range(1,334):
    print(3*x)
    sum = sum + (3*x)

print("\n")
for x in range(1,200):
    if((5*x)%3 != 0):
        print(5*x)
        sum = sum + (5*x)

print(sum)
