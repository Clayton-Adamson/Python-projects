"""
PE 41:

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once.
For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?

"""

# I'm not sure if an n-digit number can make use of more than 9 digits
# I'll try it with just 9

import math
import time

start_time = time.time()


# checks if all the digits are represented
def check_pandigital(num):

    conversion = str(num)
    length = len(conversion)

    for x in range(1,length+1):
        if(str(x) not in conversion):
            return 0

    return num


# Now let's generate primes

primes = [2,3,5,7,11]


#I AM SO GLAD THAT ANSWER < 10 MILLION
# I tried to run this at 100 million to reach 9 digits...
# it didn't terminate after 90 min.

answer = 0
for x in range(13,10000000):
    for y in primes:
        if(x%y == 0):
            break
        elif(y>math.sqrt(x)):
            primes.append(x)
            if(check_pandigital(x) != 0):
                answer = x
            break

'''
for x in range(13,10000000):
    for y in primes:
        if(x%y == 0):
            break
        elif(y>math.sqrt(x)):
            primes.append(x)
            break

answer = 0
for x in primes:
    if(check_pandigital(x) > answer):
        answer = x
'''
print(answer)
print("--- %s seconds ---" % (time.time() - start_time))

# I can't figure out which of these methods is better
# The times vary
