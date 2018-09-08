"""
PE 36:

The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)
"""

#SLICING WOOP WOOP!

# checks if base 10 is palindrome
def dec_pal(num):
    conversion = str(num)
    if(conversion == conversion[::-1]):
        return True

    else:
        return False


# checks if base 2 is palindrome
def bin_pal(num):
    conversion = bin(num)[2:]

    if(conversion == conversion[::-1]):
        return True

    else:
        return False


count = 0
for x in range(1,1000000):
    if(dec_pal(x) and bin_pal(x)):
        count += x

print(count)
