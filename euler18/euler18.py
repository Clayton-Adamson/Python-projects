# PE 18: Given a pyramid of numbers, find the largest sum possible after
# tracing a path from top to bottom (like a pachinko game, each number only
# connects to the 2 below it)

import random

num_list = [[75], [95, 64], [17, 47, 82], [18, 35, 87, 10], [20, 4, 82, 47, 65],
[19, 1, 23, 75, 3, 34], [88, 2, 77, 73, 7, 63, 67], [99, 65, 4, 28, 6, 16, 70, 92],
[41, 41, 26, 56, 83, 40, 80, 70, 33], [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
[53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14], [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
[91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48], [63, 66, 4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
[4, 62, 98, 27, 23, 9, 70, 98, 73, 93, 38, 53, 60, 4, 23]]



# This code is a little confusing because each added number requires knowing
# the index of the previous number. The first for loop is to brute force the problem.


max_sum = 0;

for x in range(0,10000):

    sum = 75;
    prev_index = 0;


    for i in range(1,15):

        pachinko = random.randint(0,1);

        sum += num_list[i][prev_index + pachinko]
        prev_index += pachinko

    if(sum > max_sum):
        max_sum = sum;


print(max_sum)
