'''
PE 25:
The Fibonacci sequence is defined by the recurrence relation:

Fn = Fn−1 + Fn−2, where F1 = 1 and F2 = 1.
What is the index of the first term in the Fibonacci sequence to contain 1000 digits?
'''

# Easy but fun

def fib(x,y):
    return x+y

a=1
b=1
counter = 2

while(True):

    if(len(str(a)) == 1000 or len(str(b)) == 1000):
        print(counter)
        break

    c = fib(a,b)
    a=b
    b=c
    counter += 1
