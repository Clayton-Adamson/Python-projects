
# PE 12
# what is the first triangle number (1+2+3+... = tri-num) to have over 500 divisors
#WOW THIS CODE IS UGLY but i still got it right
import sys
import random
import math


def tri_num(x):
    sum_num = 0
    for i in range(1,x+1):
        sum_num = i + sum_num

    return(sum_num)

def factor(x):
    factor_list = []
    for i in range(1,int(math.sqrt(x)+1)):
        if(x % i == 0 and i not in factor_list):
            factor_list.append(i)

    print(str(x) + " has " + str(2*len(factor_list)) + " factors")
    print("\n")
    return(2*len(factor_list))
    #math-wise this^^ is ugly but we luck out 

max_factors = 0

for x in range(29,20000):
    factor(tri_num(x))
    if(factor(tri_num(x))>max_factors):
        max_factors = factor(tri_num(x))
    if(max_factors>500):
        print(str(tri_num(x)) + " is our first guess")
        break
       
       # it's a guess because there could be a square in the factorization,
       # leading to an odd number of factors (answer has even num of factors)
        

print(tri_num(12375))
