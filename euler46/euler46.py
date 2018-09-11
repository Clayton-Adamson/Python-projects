"""
PE: 46

It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.

9 = 7 + 2×1^2
15 = 7 + 2×2^2
21 = 3 + 2×3^2
25 = 7 + 2×3^2
27 = 19 + 2×2^2
33 = 31 + 2×1^2

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
"""
import math

#first I make 3 lists: primes, comps, and squares

primes = [2, 3, 5, 7, 11]
upper_limit = 10001

for x in range(12,upper_limit):
    for y in primes:

        if(x%y == 0):
            break

        elif(y>math.sqrt(x)):
            primes.append(x)
            break


comp_list = []

for x in range(9,upper_limit):

    if(x in primes or x%2 ==0):
        continue

    else:
        comp_list.append(x)


squares = []

for x in range(1,int((math.sqrt(upper_limit/2)))+2):
    squares.append(2*int(math.pow(x,2)))

# where the magic happens
def check_comp(comp,squares,primes):

    for p in primes:

        if(p>comp):
            return comp

        for s in squares:

            if(s>comp):
                break

            elif(p+s == comp):
                return 0


for x in comp_list:

    if(check_comp(x,squares,primes) != 0):
        print(x)
        break
