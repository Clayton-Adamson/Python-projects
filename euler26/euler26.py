"""
PE 26:
A unit fraction contains 1 in the numerator.
 The decimal representation of the unit fractions with denominators 2 to 10 are given:

1/2	= 	0.5
1/3	= 	0.(3)
1/4	= 	0.25
1/5	= 	0.2
1/6	= 	0.1(6)
1/7	= 	0.(142857)
1/8	= 	0.125
1/9	= 	0.(1)
1/10	= 	0.1
Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle.
It can be seen that 1/7 has a 6-digit recurring cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.
"""

#SUCCESS! sorta... there was a lot of junk code that I cut out after solving, 
# but it still takes some time to compile

def long_division(num,denom):
    dec_expansion = ""
    while(len(dec_expansion) < 3001):

        if(denom > num):
            dec_expansion += "0"
            num *= 10

        dec_expansion += str(num//denom)
        remainder = num - (num//denom)*denom
        num = remainder * 10

    return dec_expansion


decimal_list = []

for x in range(2,1000):
    decimal_list.append([x, long_division(1,x)[1::]])

#   gets rid of the pesky one's place zero    ^^^^^

def check_cycle(decimal, gap):
    for x in range(0,(len(decimal) - 3*gap)):
        if(decimal[x : x+gap] == decimal[x+gap : x+(2*gap)] and decimal[x : x+gap] == decimal[x+(2*gap) : x+(3*gap)]):
            return gap

        if(x == len(decimal) - (3*gap)-1):
            return 0

answer = 0
biggest_gap = 0

for x in range(0, len(decimal_list)):
    for gap in range(2,1001):
        repeat = check_cycle(decimal_list[x][1],gap)

# I'm not exactly sure why, but trying to simplify
# these next 2 if statements into one DESTROYS the program's speed

        if(repeat != 0):
            if(repeat > biggest_gap):
                biggest_gap = repeat
                answer = decimal_list[x][0]
                print(answer)
            break

print("answer is 1/" + str(answer))
