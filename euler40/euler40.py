"""
PE: 40

An irrational decimal fraction is created by concatenating the positive integers:
0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value of the following expression.
d1 × d10 × d100 × d1000 × d10000 × d100000 × d1,000,000
"""
import math

giant_string = ""
count = 1

while(len(giant_string) < 1000000):
    giant_string += str(count)
    count += 1

answer = 1
for x in range(0,7):
    answer *= int(giant_string[int(math.pow(10,x))-1])

print(answer)
