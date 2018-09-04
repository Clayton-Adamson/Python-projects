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


# counter plus 2 gives the result, note that 
# the while loop prints a fib_sum over 4 million, but this value is odd,
# so the if statement throws it out of the counter

print(counter)
