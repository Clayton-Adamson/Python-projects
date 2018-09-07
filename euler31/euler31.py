"""
PE 31:
In England the currency is made up of pound, £, and pence,
 p, and there are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p).
It is possible to make £2 in the following way:

1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
How many different ways can £2 be made using any number of coins?
"""
# DONT JUDGE MEEEEEEEEEEEEEE,
# omg this code is so ugly
# ok judge me


# each of the 8 coins can divide 200 equally
permutations = 8
# max iterations of each coin from 1 pence to 1 pound: 200,100,40,20,10,4,2
# each nested for loop is a degree of shame

for a in range(0,2):
    for b in range(0,4):
        for c in range(0,10):
            for d in range(0,20):
                for e in range(0,40):
                    for f in range(0,100):
                        for g in range(0,200):
                                sum = (100*a) + (50*b) + (20*c) + (10*d) + (5*e) + (2*f) + g
                                if(sum == 200):
                                    permutations += 1
                                    break
                                elif(sum > 200):
                                    break
print(permutations)
