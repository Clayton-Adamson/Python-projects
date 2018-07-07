import sys
import random
import math

# PE 1
# Find the sum of all multiples of 3 or 5 below 1000


sum = 0
for x in range(1,334):
    print(3*x)
    sum = sum + (3*x)

print("\n")
for x in range(1,200):
    if((5*x)%3 != 0):
        print(5*x)
        sum = sum + (5*x)

print(sum)


# PE 2
# find the sum of the even fibonacci numbers under 4 million

fib1 = 1
fib2 = 2
fib_sum = 0
counter = 0

while(fib_sum<=4000000):

    fib_sum = fib1 + fib2
    print(fib_sum)
    fib1=fib2
    fib2 = fib_sum
    if(fib_sum%2==0):
        counter = counter + fib_sum

print("\n")


# counter plus 2 gives result, note that 
# the while loop prints a fib_sum over 4 million, but this value is odd,
# so the if statement throws it out of the counter

print(counter)



# PE 3
#find largest prime of an ugly number

answer = 600851475143


for x in range(2,answer):
    if(answer % x == 0):
        answer = answer/x
        print(x)
        print(answer)
        print("\n")
        if(answer == 1):
            break

print("made it out")
print(71*839*1471*6857/600851475143)
print("done")

#assumed that breaking down the larger number would lead to prime



# PE 4
# Find largest palindrome from the product of 3 digit numbers

master_list = []

def pal(a,b):
    num = a*b
    if(num>100000 and num<999999):

        num_list = []
        f_list = []
        l_list = []

        for x in str(num):
            num_list.append(x)

        for x in range(0,3):
            f_list.append(num_list[x])

        for x in range(5,2,-1):
            l_list.append(num_list[x])

        for x in range(0,3):
            if(f_list[x] != l_list[x]):
                break
            elif(f_list[x] == l_list[x] and x==2):
                print(num)
                print("\n")
                master_list.append(num)



for x in range(100,999):
    for y in range(100,999):
        pal(x,y)

# I wish I made it so that i didn't need the master list outside the method, but w/e
print(max(master_list))




# PE 5
# smallest positive number evenly divisible by all numbers 1 to 20
# figured this out manually first, solution is built on manual method
# IDC HARDCODING THIS WAS FASTER :P

ans = 1*2*3*5*7*11*13*17*19*2*2*3*2
print(ans)


# PE 6
# Find the difference between the first hundred sum of the squares
#  and the first one hundred square of the sum


sum_sq = 0
sq_sum = 0

for x in range(1,101):
    sum_sq = sum_sq + x**2
    sq_sum = sq_sum + x

print(sq_sum**2 - sum_sq)




# PE 7
# What is the 10001 prime number

primes = [2,3,5,7,11,13]

for x in range(14,105000):
    for y in range(int(x/2),1,-1):
        if(x % y == 0):
            x=x+1
            break

        elif((x % y != 0) and (y==2)):
            primes.append(x)
            print(str(x) + " is the " + str(len(primes)) + " prime" )
            x=x+1
            continue


print("\n")
print(str(len(primes)) + " primes found")

print(primes[10000])



# PE 8
# 1000 digit number

giant_num = 7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450

giant_list = [int(x) for x in str(giant_num)]
answer = 0


for x in range(0,988):
    sol = 1

    for y in range(x,(x+13)):
        sol = sol*giant_list[y]

    if(sol>=answer):
        answer = sol
        print(x)
        print(answer)

print("\n")
print(answer)

#[int(x) for x in str(n)] is INVALUABLE for converting ints to lists

        

# PE 9
# pythagorean triplet, find product abc
# when a+b+c = 1000

for a in range(1,1000):
    for b in range(2,1001):
        if(a>b):
            continue
        else:
            hyp = a**2 + b**2

            if(a + b + pow(hyp,0.5) >= 1001):
                continue
            elif(a + b + pow(hyp,0.5) == 1000):
                print(str(a + b + pow(hyp,0.5)) + " " + str(a) + " " + str(b))
                print(a*b*pow(hyp,0.5))


# PE 10
# sum of primes below 2 million


sum_primes = 17
prime_list = [2,3,5,7]

for x in range(11,2000000):
    for y in range(0, len(prime_list)):
        if(x % prime_list[y] == 0):
            break

        elif(prime_list[y]>int(x/3)):
            prime_list.append(x)
            sum_primes = sum_primes + x
           # print(str(x) + " is the " + str(len(prime_list)) +  " prime")
            break

print("The sum of primes equals " + str(sum_primes))



# PE 11 "grid hell"
# Largest product of 4 numbers vert, horiz, and diag in grid (like a crossword)


grid_hell = [[8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8],
[49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48, 4, 56, 62, 0],
[81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30, 3, 49, 13, 36, 65],
[52, 70, 95, 23, 4, 60, 11, 42, 69, 24, 68, 56, 1, 32, 56, 71, 37, 2, 36, 91],
[22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
[24, 47, 32, 60, 99, 3, 45, 2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
[32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
[67, 26, 20, 68, 2, 62, 12, 20, 95, 63, 94, 39, 63, 8, 40, 91, 66, 49, 94, 21],
[24, 55, 58, 5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
[21, 36, 23, 9, 75, 0, 76, 44, 20, 45, 35, 14, 0, 61, 33, 97, 34, 31, 33, 95],
[78, 17, 53, 28, 22, 75, 31, 67, 15, 94, 3, 80, 4, 62, 16, 14, 9, 53, 56, 92],
[16, 39, 5, 42, 96, 35, 31, 47, 55, 58, 88, 24, 0, 17, 54, 24, 36, 29, 85, 57],
[86, 56, 0, 48, 35, 71, 89, 7, 5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
[19, 80, 81, 68, 5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77, 4, 89, 55, 40],
[4, 52, 8, 83, 97, 35, 99, 16, 7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
[88, 36, 68, 87, 57, 62, 20, 72, 3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
[4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18, 8, 46, 29, 32, 40, 62, 76, 36],
[20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74, 4, 36, 16],
[20, 73, 35, 29, 78, 31, 90, 1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57, 5, 54],
[1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52, 1, 89, 19, 67, 48]]



# prod will be final answer
prod = 1


# All horizontal products
for y in range(0, 20):
    for x in range(0, 17):
        counter = 1
        for i in range(x, x + 4):
            counter = grid_hell[y][i] * counter

        if(counter>prod):
            prod = counter


# All Vertical products
for y in range(0, 20):
    for x in range(0, 17):
        counter = 1
        for i in range(x, x + 4):
            counter = grid_hell[i][y] * counter

        if(counter>prod):
            prod = counter


# top left to bottom right diag
for y in range(0, 17):
    for x in range(0, 17):
        counter = 1
        for i in range(0,4):
            counter = grid_hell[y + i][x + i] * counter

        if(counter>prod):
            prod = counter
            print(prod)


# top right to bottom left diag
#final answer comes from this sequence because of course I did this last
for y in range(16, -1, -1):
    for x in range(19, 2, -1):
        counter = 1
        for i in range(0,4):
            counter = grid_hell[y + i][x - i] * counter

        if(counter>prod):
            prod = counter
            print(prod)

# prints final answer
print(prod)



# PE 12
# what is the first triangle number (1+2+3 = 6) to have over 500 divisors
#WOW THIS CODE IS UGLY but i still got it right

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
    #math-wise this^^ is ugly but shhhhhh cause it still works

max_factors = 0

for x in range(29,20000):
    factor(tri_num(x))
    if(factor(tri_num(x))>max_factors):
        max_factors = factor(tri_num(x))
    if(max_factors>500):
        print(str(tri_num(x)) + " is our first guess")
        #it's a guess because there could be a square in the factorization
        break

print(tri_num(12375))



