"""
PE 38:

Take the number 192 and multiply it by each of 1, 2, and 3:

192 × 1 = 192
192 × 2 = 384
192 × 3 = 576
By concatenating each product we get the 1 to 9 pandigital, 192384576.
We will call 192384576 the concatenated product of 192 and (1,2,3)

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5,
giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated
product of an integer with (1,2, ... , n) where n > 1?
"""
import time

start_time = time.time()


# Initial idea, probably saves time to block all bad numbers
# at this point. Might scrap this
def not_nine(num):
    test = str(num)

    if(test[0] != "9"):
        return True

    else:
        return False


# If I were smarter I wouldn't need a count variable. I am not smarter... yet!
def join_digits(num):

    answer = ""
    count = 1
    while(len(answer) < 9):

        sub_num = count * num
        answer += str(sub_num)

        if(count == 1 and not_nine(sub_num)):
            return 0

        count += 1

    if(len(answer) == 9):
        return int(answer)

    else:
        return 0

#Checks if 1 through 9 is in a number
def check_pan(num):

    num_list = ['1','2','3','4','5','6','7','8','9']
    test_num = str(num)

    for x in num_list:

        if(x not in test_num):
            return False

    return True

# Given in question
largest_product = 918273645

#Technically the range second arg should be bigger, but it works at 10,000
# tl;dr a hundredth of a second is better than 3 minutes
for x in range(1,10000):
    y = join_digits(x)
    if(y > 0 and check_pan(y)):
        if(y > largest_product):
            largest_product = y

print(largest_product)
print("--- %s seconds ---" % (time.time() - start_time))
