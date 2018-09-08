"""
PE 37:
The number 3797 has an interesting property. Being prime itself,
it is possible to continuously remove digits from left to right,
and remain prime at each stage: 3797, 797, 97, and 7.
Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""

import math

# First let's generate primes
primes = [2,3,5,7,11]

for x in range(12,800000):
    for y in primes:
        if(x%y == 0):
            break

        elif(y > int(math.sqrt(x))):
            primes.append(x)
            break


# truncates from left to right
def left_chop(num):

    length = len(str(num)) - 1
    divisor = math.pow(10, length)
    chopped_list = []

    for x in range(0,length):
        chopped_num = num%divisor
        chopped_list.append(int(chopped_num))
        divisor /= 10
        num = chopped_num

    return chopped_list


# truncates from right to left
def right_chop(num):
    
    chopped_list = []
    length = len(str(num)) - 1
    
    for x in range(0,length):
        chopped_num = num // 10
        chopped_list.append(int(chopped_num))
        num = chopped_num

    return chopped_list
    

# checks if all elements in a list are prime
def check_prime(potential_prime_list, reference):

    for x in potential_prime_list:
        if(x not in reference):
            return False

    return True


answer_list = []
for x in primes:
    if(check_prime(right_chop(x), primes) and check_prime(left_chop(x), primes)):
        answer_list.append(x)

for x in answer_list:
    print(x)


count = 0

for x in answer_list:
    count += x

# subtract 17 so the single digit primes don't get counted
print(count-17)
