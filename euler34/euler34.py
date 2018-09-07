"""
PE 34:
145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: as 1! = 1 and 2! = 2 are not sums they are not included.
"""

import math

def split_int(num):

    sum = 0
    conversion = str(num)
    for char in conversion:
        sum += math.factorial(int(char))
    return sum

answer_sum = 0
max_curious = 0

#Turns out they're only asking us to
# find a single number, which is < 41,000

for x in range(3,100000):
    if(x == split_int(x)):
        answer_sum += x
        max_curious = x

print(answer_sum)
print(max_curious)
