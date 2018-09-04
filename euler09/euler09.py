# PE 9
# pythagorean triplet, find product abc
# when a+b+c = 1000

import sys
import random
import math

for a in range(1,1000):
    for b in range(2,1001):
        if(a>b):
            continue
        else:
            hyp = a**2 + b**2

            if(a + b + pow(hyp,0.5) >= 1001):
                continue
            elif(a + b + pow(hyp,0.5) == 1000):
                print(str(a + b + pow(hyp,0.5)) + " " + str(a) + " " + str(b))
                print(a*b*pow(hyp,0.5))
