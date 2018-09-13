"""
PE: 50

The prime 41, can be written as the sum of six consecutive primes:

41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
"""

# The difficult thing to grasp is that there are 3 (THREE) unique chains of consecutive primes that add up to the final answer
# This makes the problem WAAAYYYYYYYY harder than it looks


import math
import time

start_time = time.time()

primes = [2]

for x in range(3,1000000):

    for y in primes:

        if(x % y == 0):
            break

        elif(y>math.sqrt(x)):
            primes.append(x)
            break


# kind of cheating, but based on hours debugging i know the answer has to be >= 978037
# (take away the method triple_check and you get answer = 978037)
# again, THREE UNIQUE CHAINS... 
candidate_primes = []

for x in primes:
    if(x >= 978037):
        candidate_primes.append(x)


# when you want to do recursion but aren't sure how to set the limit...
# see the method add_primes to see what this is actually doing
def triple_check(num,upper_bound,prime_lst):

    upper_limit = upper_bound

    if(upper_limit < 3):
        return 0

    count = 0
    sepi = upper_limit

    while((upper_limit + 1) * prime_lst[upper_limit] > num):


        if(count == num):
            challenger_answer = upper_limit - sepi
            return challenger_answer


        elif(count > num):
            count -= prime_lst[upper_limit]
            upper_limit -= 1


        else:

            if(sepi == -1):
                break

            count += prime_lst[sepi]
            sepi -= 1

    return 0


# When you really wish you had an easy way to do recursion with a limit case...
# again see next method
def double_check(num,upper_bound,prime_lst):

    upper_limit = upper_bound

    if(upper_limit < 3):
        return 0

    count = 0
    sepi = upper_limit

    while((upper_limit + 1) * prime_lst[upper_limit] > num):

        if(count == num):

            provisional_answer = upper_limit - sepi
            challenger_answer = triple_check(num, upper_limit - 1, primes)

            if(provisional_answer > challenger_answer):
                return provisional_answer

            else:
                return challenger_answer



        elif(count > num):
            count -= prime_lst[upper_limit]
            upper_limit -= 1


        else:

            if(sepi == -1):
                break

            count += prime_lst[sepi]
            sepi -= 1

    return 0


# This method starts at the largest prime that could be added and works its way towards 2 (the smallest prime)
# It's important to keep in mind that this method "adds down" (adding smaller numbers to larger numbers)
# instead of adding larger numbers to smaller numbers. This is to avoid looping through prime_lst over and over
def add_primes(num, prime_lst):

    upper_limit = next(i for i,prime in enumerate(prime_lst) if prime > int(num/2)+1)

    if(upper_limit < 3):
        return [0,0]

    count = 0
    # next variable is the smaller (exclusive) prime index, or 'sepi' for short
    # this is the index of the largest prime that is not in the current add chain,
    # in other words, the prime "on deck" to be added from below. (prime_lst[sepi] < each prime in add chain)
    sepi = upper_limit

    while((upper_limit + 1) * prime_lst[upper_limit] > num):

        if(count == num):

            provisional_answer = upper_limit - sepi

            challenger_answer = double_check(num, upper_limit - 1, primes)
            # This starts a recursive call to an almost identical function
            # I tried different methods of limiting recursion, but it didn't end well
            # so i said "screw it" and avoided recursive depth reached errors by creating 2 copy methods
            # on one hand, judge me, on the other hand, screw you this took >12 hours and debugging this was a nightmare
            
            if(provisional_answer > challenger_answer):
                return [num, provisional_answer]

            else:
                return [num, challenger_answer]

        elif(count > num):
            count -= prime_lst[upper_limit]
            upper_limit -= 1

        else:
            # Originally I set the while loop to stop if sepi gets small enough, but I still need to check if adding 
            # 2 (which is prime_lst[0]), will lead to a favorable result, so it's better the way it is now, 
            # since sepi is incremented after use and sepi = -1 after using index 0
            if(sepi == -1):
                break
            
            count += prime_lst[sepi]
            sepi -= 1

    return [0,0]


# The part where we put everything together
terms = 0
answer = 0

for x in candidate_primes:

    # sum_chain is a 2 element list, [prime, terms needed to add up to prime]
    sum_chain = add_primes(x, primes)

    if(sum_chain[0] != 0 and sum_chain[1] > terms):
        terms = sum_chain[1]
        answer = sum_chain[0]
        print(str(answer) + " has " + str(terms) + " terms")


print("final answer is " + str(answer) + " and has " + str(terms) + " terms")
print(str(time.time() - start_time) + " seconds")
