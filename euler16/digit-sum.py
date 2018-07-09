# PE 16
# sum of digits in 2^1000

big_num = 2**1000
big_list = [int(x) for x in str(big_num)]
counter = 0

for x in range(0,len(big_list)):
    counter = counter + big_list[x]

print(counter)
