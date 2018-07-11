# Euler 4
import sys
maxPal = 0
for a in range(100,999):
    for b in range(100,999):
        c=a*b
        if str(a*b)== str(a*b)[::-1] and c > maxPal: # look this up! Python list indexing is awesome!
            maxPal = c
print(maxPal)
