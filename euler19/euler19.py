'''
PE 19:
You are given the following information, but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days has September,
April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.
A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?
'''

# From 1st to 1st Table:
# 31 -> +3 days of the week
# 30 -> +2
# 29 -> +1
# 28 -> +0

months = [3,0,3,2,3,2,3,3,2,3,2,3]

leap_months = [3,1,3,2,3,2,3,3,2,3,2,3]

# days are labeled 1,2,3,4,5,6,7

#start on monday
d = 2

sunday_sum = 0

for i in range(1900,2001):

    if(i>1900 and i%4 == 0):

        for x in leap_months:

            if(d==1):
                sunday_sum += 1

            d += x

            if(d>7):
                 d = d-7

    else:

        for x in months:


            #Those sneaky bastards didn't count 1900, they start at 1901.
            #Otherwise this code would have been perfect on the first try.
            #This for loop cycles through 1900 to keep the day of the
            #week accurate, but the next if statement doesn't count the 1900 sunday months.
            if(d==1 and i>1900):
                sunday_sum += 1

            d += x

            if(d>7):
                 d = d-7

print(sunday_sum)
