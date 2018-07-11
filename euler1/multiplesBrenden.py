# PE 1
# Find the sum of all multiples of 3 or 5 below 1000

# Get in the habit of not including import unless necessary
sum = 0
for x in range(0,1000,3): # you can use range to count by a number
    sum = sum + x
for x in range(0,1000,5):
    if(x%3 != 0):
        sum = sum + x
print(sum)
