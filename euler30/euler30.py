"""
PE 30:
Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

1634 = 14 + 64 + 34 + 44
8208 = 84 + 24 + 04 + 84
9474 = 94 + 44 + 74 + 44
As 1 = 14 is not a sum it is not included.

The sum of these numbers is 1634 + 8208 + 9474 = 19316.

Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
"""
import math
import time
start_time = time.time()


def fifth_power(num):

    num_list = []

    for digits in str(num):
        num_list.append(int(digits))

    count = 0
    for x in num_list:
        count += math.pow(x,5)

    return count


answer_list = []
for x in range(2,10000000):
    if(x == fifth_power(x)):
        answer_list.append(fifth_power(x))


count = 0
for x in answer_list:
    count += x

print(count)



print("--- %s seconds ---" % (time.time() - start_time))

#condition in method: 71.541 seconds
#condition out of method: 68.69 seconds
