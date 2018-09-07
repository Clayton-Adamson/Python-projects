"""
PE 33:
The fraction 49/98 is a curious fraction,
as an inexperienced mathematician in attempting to simplify it may incorrectly believe
that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.
There are exactly four non-trivial examples of this type of fraction,
less than one in value, and containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms,
find the value of the denominator.
"""

product = 1

for num in range(10,100):
    a = num//10
    b = num%10
    for denom in range(99,9,-1):

        if(num/denom > 1):
            break

        else:
            c = denom//10
            d = denom%10

            if(c != 0 and d != 0 and num != denom):

                if(a == c and num/denom == b/d):
                    product *= num/denom
                    print(str(num) + "/" + str(denom))
                    continue

                if(b == c and num/denom == a/d):
                    product *= num/denom
                    print(str(num) + "/" + str(denom))
                    continue

                if(a == d and num/denom == b/c):
                    product *= num/denom
                    print(str(num) + "/" + str(denom))
                    continue

                if(b == d and num/denom == a/c):
                    product *= num/denom
                    print(str(num) + "/" + str(denom))
                    continue

print(product)
# answer is 0.01000000002 = 1/100 --> 100
