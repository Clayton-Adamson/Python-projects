"""
PE 39:

If p is the perimeter of a right angle triangle with integral length sides, {a,b,c},
there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximised?
"""


# I like this code, I got the right answer on the first try
import math

squares = []

for x in range(1,1001):
    squares.append(int(math.pow(x,2)))

# checks if the hypotenuse is an integer
def check_hyp(hyp_squred,squares_list):

    if(hyp_squred in squares_list):
        return int(math.sqrt(hyp_squred))

    else:
        return 0

perimeter_list = []
for x in range(0,1000):
    perimeter_list.append([x+1,0])

max_solutions = 0
answer = 0

for a in range(2,1000):
    for b in range(1,a+1):

        c_squared = math.pow(a,2) + math.pow(b,2)
        c = check_hyp(c_squared, squares)

        if(c != 0):
            perimeter = a + b + c

            if(perimeter <= 1000):
                perimeter_list[perimeter-1][1] += 1

                if(perimeter_list[perimeter-1][1] > max_solutions):
                    max_solutions = perimeter_list[perimeter-1][1]
                    answer = perimeter_list[perimeter-1][0]



for x in perimeter_list:
    print(x)

print(max_solutions)
print(answer)
