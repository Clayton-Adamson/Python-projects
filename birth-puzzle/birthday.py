import sys
import os
import random

# You have to input N into the console for the program to run!
# N = number of people in the room
N = sys.stdin.readline()

print("There are " + str(N) + "people in the room")

bir_list = []

for x in range(0,12):
    bir_list.append([])
    for y in range(0,31):
        bir_list[x].append(0)

print("\n")

for i in range(0,int(N)):
    x=random.randrange(0,12)
    y=random.randrange(0,31)
    bir_list[x][y] = bir_list[x][y] + 1
    i = i+1

for x in range(0,12):
    print(bir_list[x])

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
print("\n")

month_avg=0
same_bir = 0
day_array = []

for x in range(0,31):
    day_array.append(0)

for x in range(0,12):
    counter=0
    for y in range(0,31):
        day_array[y] = day_array[y] + bir_list[x][y]
        counter = counter + bir_list[x][y]
        percent=round(counter*100/int(N),2)
        if(bir_list[x][y]>1):
            same_bir = same_bir + bir_list[x][y]

        if (y==30):
            print(str(percent) + "% of birthdays were in " + months[x])
            month_avg = month_avg + percent

print("\n")

avg_days=0
for x in range(0,31):
    day_people = round(100*day_array[x]/int(N),2)
    avg_days = day_people + avg_days
    print(str(day_people) + "% of people were born on the " + str(x+1) + " day")
print("\n")

print("Average day is " + str(round(avg_days/31,2)) + "%")

print("\n")
print("Monthly average of " + str(round(month_avg/12,2)) + "%")
print("\n")



print("\n")

bir_str = str(round(100*same_bir/int(N),2))

print(str(same_bir) + " people share a birthday")
print(bir_str + "% of people share a birthday")
