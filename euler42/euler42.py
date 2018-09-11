"""
PE: 42

The nth term of the sequence of triangle numbers is given by, tn = ½n(n+1);
so the first ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its alphabetical position
and adding these values we form a word value.
For example, the word value for SKY is 19 + 11 + 25 = 55 = t10.
If the word value is a triangle number then we shall call the word a triangle word.

Using words.txt (right click and 'Save Link/Target As...'),
a 16K text file containing nearly two-thousand common English words, how many are triangle words?
"""
#The first few lines was the hardest part by far.... terminal-esque stuff is still new for me
#this def won't run on your comp, but I got the right answer

import os

os.chdir('/Users/claytonadamson/Desktop')
text_file = open('p042_words.txt', 'r')
word_list = text_file.read().split(',')
text_file.close()

triangle_list = []

#based on the length of the words, upper limit of range doesn't need to be huge
for x in range(1,30):
    num = (x/2)*(x+1)
    triangle_list.append(int(num))



def is_triangle(word, num_list):

    count = 0

    #There are quotation mark characters attached to the words, therefore slicing
    for char in word[-2:0:-1]:
        value = ord(char) - 64
        count += value

    if(count in num_list):
        return True

    else:
        return False
        

answer = 0
for words in word_list:
    if(is_triangle(words,triangle_list)):
        answer += 1

print(answer)
