"""
PE 27:
Euler discovered the remarkable quadratic formula:

n2+n+41
It turns out that the formula will produce 40 primes for the consecutive integer values 0≤n≤39.
However, when n=40,40^2+40+41=40(40+1)+41 is divisible by 41,
and certainly when n=41,41^2+41+41 is clearly divisible by 41.

The incredible formula n2−79n+1601 was discovered,
which produces 80 primes for the consecutive values 0≤n≤79.
The product of the coefficients, −79 and 1601, is −126479.

Considering quadratics of the form:

n2+an+b, where |a|<1000 and |b|≤1000

where |n| is the modulus/absolute value of n
e.g. |11|=11 and |−4|=4
Find the product of the coefficients, a and b, for the quadratic expression that produces
 the maximum number of primes for consecutive values of n, starting with n=0.
"""

# n=0 --> b, so b always has to be a prime number
# I'll start by generating all the primes below 1000, this will be my b-list
# 79 is prime...... I am suspicious.... I'll cheat and say A must be prime (it works)

import math

primes = [2]
coeff_list = [-2, 2]

for b in range(2,1000):
    for x in range(2,int(math.sqrt(b)) + 2):

        if b%x == 0:
            break

        elif x >= int(math.sqrt(b))+1:
            primes.append(b)
            coeff_list.append(-b)
            coeff_list.append(b)

max_primes = 0
coeff_A = 0
coeff_B = 0

# The line I'd use if I wasn't cheating
#for a in range(-999, 1000):

# The line that saves me time, because primes, for some reason
for a in coeff_list:

    for b in coeff_list:
        count = 0
        for n in range(0,1000):
            if n**2 + a*n + b in primes:
                count += 1
            else:
                if count >= max_primes:
                    max_primes = count
                    coeff_A = a
                    coeff_B = b

                break


print(coeff_A)
print(coeff_B)
print(coeff_A * coeff_B)


