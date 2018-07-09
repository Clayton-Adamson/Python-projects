# PE 14
# Collatz sequences (find longest sequence)
# if x is even, divide x by 2
# if x is odd, return 3x+1
# repeat until x=1

import sys
import random
import math

answer = 0

def seq(x):

    collatz = [x]

    while(True):
        if(x==1):
            return len(collatz)

        elif(x % 2 == 0):
            x=x/2
            collatz.append(x)

        else:
            x=(3*x)+1
            collatz.append(x)

# I had to find the longest sequence in this range
for x in range(1,1000000):
    if(seq(x)>answer):
        answer = seq(x)
        print(str(x) + " has a chain of " + str(answer))
