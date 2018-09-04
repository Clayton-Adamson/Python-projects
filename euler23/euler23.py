# PE 23:
'''
A perfect number is a number for which the sum of its proper divisors is exactly equal to the number.
For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.
A number n is called deficient if the sum of its proper divisors is less than n and it is called abundant if this sum exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written
as the sum of two abundant numbers is 24. By mathematical analysis,
it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers.
However, this upper limit cannot be reduced any further by analysis even though it is known that
the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit.

Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.
'''

import math
import time
start_time = time.time()

#This works, but I'm not happy with it since it takes 6 minutes


def find_abundant(num):
    factor_list = [1]
    for x in range(2, int(math.sqrt(num)) + 1):
        if(num%x == 0 and x not in factor_list):
            factor_list.append(x)
            if(x != num/x):
                factor_list.append(num/x)
    count = 0
    for x in factor_list:
        count += x
    if(count > num):
        return num

    else:
        return 0;

abundant_list = []
for x in range(1,28123):
    if(find_abundant(x) > 0):
        abundant_list.append(x)


fussy_number_list = []

for x in range(1,28123):
    for y in abundant_list:
        if(y>x-11):
            limit = abundant_list.index(y)
            break

    for y in abundant_list:
        test = x-y
        if(test in abundant_list[0:limit]):
            break
        if(y > int(x/2) + 1):
            fussy_number_list.append(x)
            break

count = 0
for x in fussy_number_list:
    count += x

print(count)


print("--- %s seconds ---" % (time.time() - start_time))
