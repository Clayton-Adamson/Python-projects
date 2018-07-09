# PE 17
# from 1,1000: how many letters used

# 1,2,3,4,5 given in question
# im manually adding one thousand and removing 9 "and"s

letters_used = ["1", "2", "3"]


def spell_ones(word,y,x):

    if(y==1):

        if(x==0):
            word.extend("ten")
        elif(x==1):
            word.extend("eleven")
        elif(x==2):
            word.extend("twelve")
        elif(x==3):
            word.extend("thirteen")
        elif(x==4):
            word.extend("fourteen")
        elif(x==5):
            word.extend("fifteen")
        elif(x==6):
            word.extend("sixteen")
        elif(x==7):
            word.extend("seventeen")
        elif(x==8):
            word.extend("eighteen")
        elif(x==9):
            word.extend("nineteen")

    else:

        if(x==1):
            word.extend("one")
        elif(x==2):
            word.extend("two")
        elif(x==3):
            word.extend("three")
        elif(x==4):
            word.extend("four")
        elif(x==5):
            word.extend("five")
        elif(x==6):
            word.extend("six")
        elif(x==7):
            word.extend("seven")
        elif(x==8):
            word.extend("eight")
        elif(x==9):
            word.extend("nine")


def spell_tens(word,y,x):

    if(y==2):
        word.extend("twenty")
    elif(y==3):
        word.extend("thirty")
    elif(y==4):
        word.extend("forty")
    elif(y==5):
        word.extend("fifty")
    elif(y==6):
        word.extend("sixty")
    elif(y==7):
        word.extend("seventy")
    elif(y==8):
        word.extend("eighty")
    elif(y==9):
        word.extend("ninety")

    spell_ones(word,y,x)



def spell_hund(word,z,y,x):

    spell_ones(letters_used, 0,z)
    word.extend("hundredand")
    spell_tens(word,y,x)



for i in range(6,10):
    spell_ones(letters_used,0,i)

for i in range(10,100):
    a_list = [int(a) for a in str(i)]
    spell_tens(letters_used, a_list[0], a_list[1])

for i in range(100,1000):
    a_list = [int(a) for a in str(i)]
    spell_hund(letters_used, a_list[0], a_list[1], a_list[2])

print(letters_used)
print(len(letters_used))
