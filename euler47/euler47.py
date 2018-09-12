"""
PE 47: 

The first two consecutive numbers to have two distinct prime factors are:

14 = 2 × 7
15 = 3 × 5

The first three consecutive numbers to have three distinct prime factors are:

644 = 2² × 7 × 23
645 = 3 × 5 × 43
646 = 2 × 17 × 19.

Find the first four consecutive integers to have four distinct prime factors each. What is the first of these numbers?
"""

import math

#Based on where the answer is, this limit is fine
upper_limit = 140000
primes = [2,3,5,7,11]

for x in range(13, upper_limit):

    for y in primes:

        if(x % y == 0):
            break

        elif(y > math.sqrt(x)):
            primes.append(x)
            break


#checks if 4 consecutive numbers are all NOT in a list
def check_consecutive(num, target):

    if(num in target or num+1 in target or num+2 in target or num+3 in target):
        return False

    else:
        return True


#checks if 4 distinct factors of num in target
def check_factors(num,target):

    factors = 0

    for x in target:
        if(num % x == 0):
            factors += 1

        elif(factors>3):
            return True

        elif(x>num/30):
            return False


#647 is prime, so let's start from 648
candidate_list = []

for x in range(648,upper_limit):

    if(check_consecutive(x,primes)):
        candidate_list.append(x)


for x in candidate_list:
    if(not check_factors(x,primes) or not check_factors(x+1,primes) or not check_factors(x+2,primes) or not check_factors(x+3,primes)):
        continue

    else:
        print(x)
        break
