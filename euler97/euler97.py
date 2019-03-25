'''
The first known prime found to exceed one million digits was discovered in 1999,
and is a Mersenne prime of the form 26972593−1; it contains exactly 2,098,960 digits.
Subsequently other Mersenne primes, of the form 2p−1, have been found which contain more digits.

However, in 2004 there was found a massive non-Mersenne prime which contains 2,357,207 digits: 28433×2^7830457+1.

Find the last ten digits of this prime number.
'''

# At first I had no idea how to do this, then I realized I can truncate a working int to ten digits

# returns int of last 10 digits of number
def truncate(num):

    digits = str(num)

    if(len(digits) > 10):
        snip = len(digits) - 10
        ans = digits[snip:]
        return int(ans)

    else:
        return num

ans = 1

for x in range(0,7830457):

    ans *= 2
    ans = truncate(ans)

ans *= 28433
ans = truncate(ans)

print(ans + 1)
