# PE 6
# Find the difference between the first hundred sum of the squares
#  and the first one hundred square of the sum


sum_sq = 0
sq_sum = 0

for x in range(1,101):
    sum_sq = sum_sq + x**2
    sq_sum = sq_sum + x

print(sq_sum**2 - sum_sq)
