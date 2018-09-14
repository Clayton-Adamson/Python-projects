"""
PE 52:
It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.
"""


# returns a list of a number's digits
def place_digits(num):

    conversion = str(num)
    digit_lst = []

    for digit in conversion:

        if(digit not in digit_lst):
            digit_lst.append(digit)

    return sorted(digit_lst)


# checks if 2 numbers have the same digits
def check_digits(target_num, test_num):

    digit_lst = place_digits(target_num)
    conversion_lst = place_digits(str(test_num))

    if(len(digit_lst) != len(conversion_lst)):
        return False

    else:
        for char in conversion_lst:
            if(char not in digit_lst):
                return False

        return True


answer = 0

for x in range(1,1000000):
    for y in range(2,7):

        if(not check_digits(x,int(y*x))):
            break

        elif(y==6):
            answer = x
            break

print(answer)
