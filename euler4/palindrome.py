# PE 4
# Find largest palindrome from the product of 3 digit numbers


# new way

max_pal = 0

def pal(num):
    for x in range(0,3):
        if(str(num)[x] != str(num)[5-x]):
            return 0
        elif(x==2):
            return num
        else:
            continue


for x in range(100,1000):
    for y in range(100,1000):
        num = x*y
        if(len(str(num)) == 6 and pal(num) > max_pal ):
            max_pal = num

print(max_pal)



'''
master_list = []

def pal(a,b):
    num = a*b
    if(num>100000 and num<999999):

        num_list = []
        f_list = []
        l_list = []

        for x in str(num):
            num_list.append(x)

        for x in range(0,3):
            f_list.append(num_list[x])

        for x in range(5,2,-1):
            l_list.append(num_list[x])

        for x in range(0,3):
            if(f_list[x] != l_list[x]):
                break
            elif(f_list[x] == l_list[x] and x==2):
                print(num)
                print("\n")
                master_list.append(num)



for x in range(100,999):
    for y in range(100,999):
        pal(x,y)

# I wish I made it so that i didn't need the master list outside the method, but w/e
print(max(master_list))
'''
