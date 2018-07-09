import random

'''
This is an extension from 131 that estimates pi using area 
I am proud/ashamed that I got it to work without 
the real numbers... The dartboard is made of a 2d list of ints
'''

x_list=[]

for i in range(0,101):
    x_list.append([])
    for j in range(0,101):
        x_list[i].append(0)

for x in range(0,101):
    for y in range(0,101):
        if((x-50)**2+(y-50)**2<=2550):
            x_list[x][y]=1

print("x list")
for x in range(0,101):
        print(x_list[x])

counter = 0
misses = 0

for i in range(0,1000000):
    num1=random.randrange(0,101)
    num2=random.randrange(0,101)
    if(x_list[int(num1)][int(num2)]==1):
        counter= counter+1
    else:
        misses= misses+1

print("\nhits")
print(counter)
print("\nmisses")
print(misses)
print("\n")

pie=(counter)*4/(misses+counter)
print("pi equals " + str(pie))
err = abs(100*(3.14159265-pie)/3.1415926)
error = round(err,2)
print("error of " + str(error)+ "%")
