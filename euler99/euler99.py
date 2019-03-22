'''
Problem 99
Comparing two numbers written in index form like 211 and 37 is not difficult,
as any calculator would confirm that 211 = 2048 < 37 = 2187.

However, confirming that 632382518061 > 519432525806 would be much more difficult,
as both numbers contain over three million digits.

Using base_exp.txt (right click and 'Save Link/Target As...'),
 a 22K text file containing one thousand lines with a base/exponent pair on each line,
 determine which line number has the greatest numerical value.

NOTE: The first two lines in the file represent the numbers in the example given above.
'''

import os
import math

os.chdir('/Users/claytonadamson/Downloads')
text_file = open('p099_base_exp.txt', 'r')
raw_lst = text_file.read().split()
text_file.close()

# separates the raw data into base-exponent pairs
def fix_num(raw_num):
    length = len(raw_num)
    split = raw_num.index(",")
    a = int(raw_num[0:split])
    b = int(raw_num[split+1:])

    return [a,b]

fixed_lst = []

for x in raw_lst:
    fixed_lst.append(fix_num(x))

ans_lst = []

# logs fix everything, no need to sift through millions of numbers
for x in fixed_lst:
    num = x[1]*math.log(x[0],10)
    ans_lst.append(num)

max_num = ans_lst.index(max(ans_lst))

print(max_num + 1)
