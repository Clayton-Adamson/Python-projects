'''
Problem 55
If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

Not all numbers produce palindromes so quickly. For example,

349 + 943 = 1292,
1292 + 2921 = 4213
4213 + 3124 = 7337

That is, 349 took three iterations to arrive at a palindrome.

Although no one has proved it yet, it is thought that some numbers, like 196, never produce a palindrome.
 A number that never forms a palindrome through the reverse and add process is called a Lychrel number.
  Due to the theoretical nature of these numbers, and for the purpose of this problem,
  we shall assume that a number is Lychrel until proven otherwise.
  In addition you are given that for every number below ten-thousand,
  it will either (i) become a palindrome in less than fifty iterations, or,
  (ii) no one, with all the computing power that exists, has managed so far to map it to a palindrome.
  In fact, 10677 is the first number to be shown to require over fifty iterations before producing a palindrome:
  4668731596684224866951378664 (53 iterations, 28-digits).

Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is 4994.

How many Lychrel numbers are there below ten-thousand?

'''

# generates reverse number of original int
def flip_num(num):

    digits = str(num)
    reverse = digits[::-1]

    return int(reverse)


# checks if num is palindrome
def check_pal(num):

    digits = str(num)
    span = len(digits)
    bisect = int(span/2)

    if(span % 2 == 0):

        first_half = digits[:bisect]
        second_half = str(flip_num(digits[bisect:]))

    else:

        first_half = digits[:bisect]

        # ignore middle digit for odd amount of digits
        second_half = str(flip_num(digits[bisect+1:]))


    if(first_half == second_half):
        return True

    else:
        return False


# did the first 9 in my head to avoid weird code for single digits
not_lychrel_total = 9

for x in range(10,10000):
    num = x
    for y in range(0,50):
        num += flip_num(num)

        if(check_pal(num)):
            not_lychrel_total += 1
            break


# answer is out of all numbers BELOW 10000
print(9999 - not_lychrel_total)

