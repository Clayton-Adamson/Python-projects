"""
PE 48:
The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
"""

# math.pow sucks

count = 0

for x in range(1,1001):
    count += int(x**x)

answer = str(count)

print(answer[-10:])

# uncomment next line for ridiculously long number, or just for the luls
# print(answer)
