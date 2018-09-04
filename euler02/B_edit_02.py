# PE 2
# find the sum of the even fibonacci numbers under 4 million

fib1 = 1
fib2 = 2
fib_sum = 0
counter = 2 # accounts for 2 as a prime (mod wont)

while(fib_sum<=4000000):
    # keep track of the orders in the while loop
    # this order makes sure the sum never accounts for something over 4000000
    # In your case it worked out because the next number was odd
    # but you want to make sure your loop accounts for exactly the problem
    if(fib_sum%2==0):
        counter = counter + fib_sum
    print(fib_sum)
    fib_sum = fib1 + fib2
    fib1=fib2
    fib2 = fib_sum

print("\n")
print(counter)
