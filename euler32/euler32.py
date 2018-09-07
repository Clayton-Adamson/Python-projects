"""
PE 32:

We shall say that an n-digit number is pandigital if it
makes use of all the digits 1 to n exactly once;
for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254,
containing multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity
can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way
so be sure to only include it once in your sum.
"""


def pandigital(a,b,c):
    number_list = ['1','2','3','4','5','6','7','8','9']
    test_string = str(a) + str(b) + str(c)

    if(len(test_string) != 9):
        return 0

    else:
        for x in number_list:
            if x not in test_string:
                return 0
        return 1

product_list = []
sum_of_products = 0


# Not exactly sure how big the ranges on these
# should be, it's not intuitive, this works though
for a in range(1,1000):
    for b in range(1,3000):
        c =a*b
        if(pandigital(a,b,c) != 1 or c in product_list):
            continue

        else:
            product_list.append(c)
            sum_of_products += c


print(product_list)
print(sum_of_products)
