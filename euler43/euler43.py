"""
PE: 43
The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order,
but it also has a rather interesting sub-string divisibility property.

Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:

d2d3d4=406 is divisible by 2
d3d4d5=063 is divisible by 3
d4d5d6=635 is divisible by 5
d5d6d7=357 is divisible by 7
d6d7d8=572 is divisible by 11
d7d8d9=728 is divisible by 13
d8d9d10=289 is divisible by 17
Find the sum of all 0 to 9 pandigital numbers with this property.
"""

#This one gave me a lot of heartache.
# At first, I didn't use itertools: I got the right answer, but it took hours.
# Technically the code never terminated... I just guessed that my partial answer could be correct (it was)

from itertools import permutations

# this line is stolen from the Euler forums... at first I had a method testing for pandigital...-ness
num_list = [int(''.join(i)) for i in sorted(list(permutations('1234567890')))]
# I didn't really understand this line at first glance, but it makes sense now
# for some reason the list method doesn't really return a normal list
# it's a bunch of tuples still... sorta, the join method fixes it though


def is_sub_div(num):

    test = str(num)
    sub_test = test[1::]
    div_list = [2,3,5,7,11,13,17]

# I think that my code is more readable... but the hardcoded multiple if-statements approach is much faster.
# I'll probably ask you about this later (are dense if-statements superior to a for loop?)
    for x in range(0,7):

        if(int(sub_test[x:x+3]) % div_list[x] != 0):
            return False

    return True

count = 0

for x in num_list:
    if(is_sub_div(x)):
        count += x

print("final answer is " + str(count))
