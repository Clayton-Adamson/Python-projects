"""
PE 24:

A permutation is an ordered arrangement of objects.
For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4.
If all of the permutations are listed numerically or alphabetically, we call it lexicographic order.
The lexicographic permutations of 0, 1 and 2 are: 012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?
"""

# I'm proud of this one because it solves it without just generating a million permutations.

import math

permutation = 1000000
digit_list = [0,1,2,3,4,5,6,7,8,9]
answer = ""

for x in range(0,10):

    digits = len(digit_list)

    for y in range(1, digits + 1):

        if(y*math.factorial(digits - 1) >= permutation):
            permutation -= (y-1)*math.factorial(digits-1)
            answer += str(digit_list[y-1])
            del digit_list[y-1]
            break

print(answer)
