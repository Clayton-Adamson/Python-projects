'''
PE 21:
Let d(n) be defined as the sum of proper divisors of n
(numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair
and each of a and b are called amicable numbers.

For example, the proper divisors of 220 are
1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284.
The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.
'''

import math

big_list = [];
ans_list = [];
final_answer = 0;

for x in range(1,10001):
    factor_list = [];
    for y in range(1,int(math.sqrt(x)+1)):
        if(x%y == 0 and y not in factor_list):
            factor_list.append(y);
            if(y != x/y):
                factor_list.append(int(x / y));
    big_list.append(factor_list);


for x in range(0,10000):
    big_list[x].sort();

for x in range(0,10000):
    print(big_list[x]);


for x in range(0,10000):

    if(big_list[x][-1] in ans_list or len(big_list[x]) == 2):
        continue

    else:
        sum1 = 0;
        sum2 = 0;

        for y in big_list[x]:
            sum1 += y;

        sum1 -= big_list[x][-1];
        twin_index = sum1 - 1;

        if(twin_index < 10001):

            for z in big_list[twin_index]:
                sum2 += z;
            sum2 -= big_list[twin_index][-1];

            if(sum2==big_list[x][-1] and twin_index != x):
                ans_list.append(big_list[x][-1]);
                ans_list.append(big_list[twin_index][-1]);
                print(ans_list);


print(ans_list);


for x in range(0, len(ans_list)):
    final_answer += ans_list[x];


print(final_answer);
