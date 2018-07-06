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
