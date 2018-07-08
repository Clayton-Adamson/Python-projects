# PE 3
#find largest prime of an ugly number

answer = 600851475143


for x in range(2,answer):
    if(answer % x == 0):
        answer = answer/x
        print(x)
        print(answer)
        print("\n")
        if(answer == 1):
            break

#assumed that breaking down the larger number would lead to prime
