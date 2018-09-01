import math


# PE 20:
# Find the sum of the digits in the number 100!


num = math.factorial(100);
sum = 0;

for x in str(num):
    sum += int(x)


print(sum)
