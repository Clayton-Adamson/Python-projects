"""
PE 35:

The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
"""

#This one took longer, but hey I got it so w/e

import math

circular_primes = [2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, 97]
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

# connecting the nested for loop to
# the primes list saves a lot of time

for x in range(30,1000000):
    for y in primes:
        if(x%y == 0):
            break
        elif(y > int(math.sqrt(x))):
            primes.append(x)
            break

# any number greater than 5 that ends with 2,4,5,6,8, or 0 will not be prime
# this method deletes any primes containing bad digits
def sift_primes(prime):

    not_prime = ['0', '2', '4', '5', '6', '8']
    test_prime = str(prime)

    for char in not_prime:
        if(char in test_prime):
            return 0

    return prime



sifted_primes = []

for x in primes:
    if(sift_primes(x) > 100):
        sifted_primes.append(x)


# creates a list of all possible rotations (cycles)
def cycle_primes(prime):

    conversion = str(prime)
    new_prime_list = []

    for x in range(1, len(conversion)):
        #HOORAY FOR SLICING!
        first_half = conversion[0:x]
        second_half = conversion[x:]
        cycle = second_half + first_half
        new_prime_list.append(int(cycle))

    return new_prime_list


# checks if all elements in a list are prime
def check_prime(potential_prime_list, reference):

    for x in potential_prime_list:
        if(x not in reference):
            return 0

    return 1



for x in sifted_primes:
    if(check_prime(cycle_primes(x), sifted_primes) != 0):
        circular_primes.append(x)


print(len(circular_primes))
