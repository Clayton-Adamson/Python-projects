
'''
Instructions:

"White" has blue pieces, black has black.
Click on the piece you want to move.
Move a piece using the blue/black selector icons.

Black player: arrow keys to move selector, Enter to confirm
White player: wasd to move selector, Space to confirm

On your turn, you can move a piece, resign (give up), or offer a draw.
If you offer a draw, the other player has to click accept draw. If they don't, play continues.

If a pawn reaches the back rank, a prompt will appear. Press q to promote to a queen.
If you're a showoff, you can instead press r for a rook, b for a bishop, or k for a knight.


Things missing from this version:

1.  50 move rule still needs to be implemented... shouldn't be that hard, just annoying

2.  Draw by 3 fold repetition might not happen... (it's not a forced draw, it has to be claimed by a player) but if it does
    i want to make a giant list that appends board postitions with booleans tacked onto the end of the list:
    [[board position], castling rights, player to move, en passant] (or just dont enter into giant list if en passant available)
    it shouldn't be hard to make a method that returns [piece type, color, x, y], and the giant list can be cleared
    to the current position upon a capture or pawn move. A separate (but loosely connected) list
    can increment the count of the position based on the index of the position in the giant list
'''


from Tkinter import *
import tkFont
import sys
import os

main = Tk()

board = Canvas(main, width = 1100, height = 650)
board.pack()


board.create_rectangle(90,90,510,510, fill = "dark grey")
board.create_rectangle(590,90,1010,510, fill = "dark grey")

# Draws the edges of the board
board.create_line(100, 100, 500, 100)
board.create_line(100, 100, 100, 500)
board.create_line(500, 100, 500, 500)
board.create_line(100, 500, 500, 500)

board.create_line(600, 100, 1000, 100)
board.create_line(600, 100, 600, 500)
board.create_line(1000, 100, 1000, 500)
board.create_line(600, 500, 1000, 500)


# Draws the Rank labels (1-8)
for x in range(0,8):
    board.create_text(65, 126 + x*50, font = "Times 19", text = str(8-x))
    board.create_text(1040, 126 + x*50, font = "Times 19", text = str(x+1))

# Draws the File labels (A-H)
board.create_text(300, 545, font = "Times 19", text = "A        B        C        D        E        F        G        H")
board.create_text(800, 545, font = "Times 19", text = "H        G        F        E        D        C        B        A")

# Draws invisible text that will prompt the user to press keys for promotion (text will appear when promote = True)
white_promote_text = board.create_text(300,50, text = "Press Q, R, B, or K to promote to a Queen, Rook, Bishop, or Knight", fill = "")

# Draws invisible text that will prompt the user to press keys for promotion (text will appear when promote = True)
black_promote_text = board.create_text(800,50, text = "Press Q, R, B, or K to promote to a Queen, Rook, Bishop, or Knight", fill = "")


# Draws invisible text that will inform the user that one player has offered a draw

white_draw_text = board.create_text(800,50, text = "White has offered a draw. Click Accept Draw or politely decline.", fill = "")

black_draw_text = board.create_text(300,50, text = "Black has offered a draw. Click Accept Draw or politely decline.", fill = "")


# Draws the squares of the board. Each square is 50X50 units
# First we create a grid with 0's representing white squares, 1's representing dark squares

helper_row = [0,1,0,1,0,1,0,1,0]
color_grid = []

for x in range(0,8):

    if(x%2 == 0):
        color_grid.append(helper_row[0:8])

    else:
        color_grid.append(helper_row[1:])

# Now we use the 2d color list to fill in the squares with the correct color
for y in range(0,8):


    for x in range(0,8):

        if(color_grid[y][x] == 1):
            board.create_rectangle(100 + 50*x, 100 + 50*y, 150 + 50*x, 150 + 50*y, fill = "grey60")
            board.create_rectangle(600 + 50*x, 100 + 50*y, 650 + 50*x, 150 + 50*y, fill = "grey60")

        else:
            #lightgoldenrod2
            board.create_rectangle(100 + 50*x, 100 + 50*y, 150 + 50*x, 150 + 50*y, fill = "white")
            board.create_rectangle(600 + 50*x, 100 + 50*y, 650 + 50*x, 150 + 50*y, fill = "white")


left_red_highlighter = board.create_rectangle(300,450,350,500)
right_red_highlighter = board.create_rectangle(750,450,800,500)

# Creates the yellow highlighter square that shows which piece has been clicked
white_yellow_highlighter = board.create_rectangle(100,100,150,150)
black_yellow_highlighter = board.create_rectangle(600,100,650,150)




# Creates the invisible squares that "light up" to show the available attack squares for the clicked piece
white_highlight_lst = []
black_highlight_lst = []

# Converts the x coordinate into the inverted version
#  (I don't add 500 in this method because sometimes I'm trying to go from the right board to the left)
def dummy_convert(num):

    dummy_lst = [100,150,200,250,300,350,400,450]
    reverse_lst = dummy_lst[::-1]

    for x in range(0,8):
        if(num == dummy_lst[x]):
            return reverse_lst[x]


def set_white_highlight_squares():

    for y in range(0,8):
        for x in range(0,8):
            square = board.create_rectangle(100 + 50*x, 100 + 50*y, 150 + 50*x, 150 + 50*y, fill = "")
            white_highlight_lst.append(square)

set_white_highlight_squares()


def set_black_highlight_squares():

    for y in range(0,8):
        for x in range(0,8):
            square = board.create_rectangle(600 + 50*x, 100 + 50*y, 650 + 50*x, 150 + 50*y, fill = "")
            black_highlight_lst.append(square)

set_black_highlight_squares()

# Method that standardizes any coordinate to a square's top left corner
def adj_coord(raw_num):

    b = 0

    for a in range(1,9):
        if(raw_num < 100 + a*50):
            b = 50 + (a*50)
            return b

# strictly for x dummy coords
def adj_dummy_coord(raw_num):

    b = 0

    for a in range(1,9):
        if(raw_num < 600 + a*50):
            b = 550 + (a*50)
            return b

def white_offer_draw():
    global white_to_move
    global black_offered_draw
    global white_offered_draw
    global game_in_progress
    global master_piece
    global promote


    if(promote):
        return

    elif(black_offered_draw and game_in_progress):
        board.itemconfig(black_draw_text, fill = "")
        master_piece = None
        game_in_progress = False

        board.create_text(550,50, text = "Draw by Agreement", fill = "black")

        small_font = tkFont.Font(family = 'Helvetica', size = 11)

        replay = Button(main, text="Rematch", command = play_again, font = small_font)
        quitt = Button(main, text="Quit", command = quit_game)
        replay.place(x = 550, y = 275, anchor = CENTER)
        quitt.place(x = 550, y = 325, anchor = CENTER)

    elif(white_to_move and game_in_progress):
        white_offered_draw = True
        board.itemconfig(white_draw_text, fill = "black")

    else:
        return


def black_offer_draw():
    global white_to_move
    global black_offered_draw
    global white_offered_draw
    global game_in_progress
    global master_piece
    global promote

    if(promote):
        return

    elif(white_offered_draw and game_in_progress):
        board.itemconfig(white_draw_text, fill = "")
        master_piece = None
        game_in_progress = False

        board.create_text(550,50, text = "Draw by Agreement", fill = "black")

        small_font = tkFont.Font(family = 'Helvetica', size = 11)

        replay = Button(main, text="Rematch", command = play_again, font = small_font)
        quitt = Button(main, text="Quit", command = quit_game)
        replay.place(x = 550, y = 275, anchor = CENTER)
        quitt.place(x = 550, y = 325, anchor = CENTER)

    elif(not white_to_move and game_in_progress):
        black_offered_draw = True
        board.itemconfig(black_draw_text, fill = "black")

    else:
        return


def white_resign():
    global white_to_move
    global game_in_progress
    global master_piece
    global promote

    if(white_to_move and game_in_progress and not promote):
        board.itemconfig(white_draw_text, fill = "")

        master_piece = None
        game_in_progress = False

        board.create_text(550,50, text = "White Resigned: Black Wins", fill = "black")

        small_font = tkFont.Font(family = 'Helvetica', size = 11)

        replay = Button(main, text="Rematch", command = play_again, font = small_font)
        quitt = Button(main, text="Quit", command = quit_game)
        replay.place(x = 550, y = 275, anchor = CENTER)
        quitt.place(x = 550, y = 325, anchor = CENTER)

    else:
        return

def black_resign():
    global white_to_move
    global game_in_progress
    global master_piece

    if(not white_to_move and game_in_progress and not promote):
        board.itemconfig(black_draw_text, fill = "")
        master_piece = None
        game_in_progress = False

        board.create_text(550,50, text = "Black Resigned: White Wins", fill = "black")

        small_font = tkFont.Font(family = 'Helvetica', size = 11)

        replay = Button(main, text="Rematch", command = play_again, font = small_font)
        quitt = Button(main, text="Quit", command = quit_game)
        replay.place(x = 550, y = 275, anchor = CENTER)
        quitt.place(x = 550, y = 325, anchor = CENTER)

    else:
        return


white_draw = Button(main, text="Offer/Accept Draw", command = white_offer_draw)
black_draw = Button(main, text="Offer/Accept Draw", command = black_offer_draw)
white_draw.place(x = 240, y = 600, anchor = CENTER)
black_draw.place(x = 740, y = 600, anchor = CENTER)


white_surrender = Button(main, text="Resign", command = white_resign)
black_surrender = Button(main, text="Resign", command = black_resign)
white_surrender.place(x = 385, y = 600, anchor = CENTER)
black_surrender.place(x = 885, y = 600, anchor = CENTER)




# These are the piece classes

# Creates a pawn, (x,y) are the top-left coordinates of the square
class pawn:

    global board
    global white_piece_coord_lst
    global black_piece_coord_lst

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.pawn_top = board.create_oval(x+18,y+11,x+32,y+25, fill = color, outline = color)
        self.pawn_base = board.create_polygon(x+25, y+20, x+35, y+40, x+15, y+40, fill = color, outline = color)
        # issoo beautiful
        self.widget_lst = [self.pawn_top, self.pawn_base]
        self.type = "pawn"

        self.move_lst = []
        self.attack_lst = []

        self.dummy_x = dummy_convert(self.x)
        self.dummy_y = dummy_convert(self.y)

        self.dummy_top = board.create_oval(self.dummy_x+518,self.dummy_y+11,self.dummy_x+532,self.dummy_y+25, fill = color, outline = color)
        self.dummy_base = board.create_polygon(self.dummy_x+525, self.dummy_y+20, self.dummy_x+535, self.dummy_y+40, self.dummy_x+515, self.dummy_y+40, fill = color, outline = color)
        self.dummy_lst = [self.dummy_top, self.dummy_base]


    def get_x(self):
        current_x = adj_coord(board.coords(self.pawn_top)[0])
        return current_x

    def get_y(self):
        current_y = adj_coord(board.coords(self.pawn_top)[1])
        return current_y


    def set_move_squares(self):

        self.move_lst = []
        x = adj_coord(board.coords(self.pawn_top)[0])
        y = adj_coord(board.coords(self.pawn_top)[1])


        if(self.color == "black"):


            enemy = white_piece_coord_lst

            # down-left (black moves down the board)
            if(x > 100 and y < 450 and ([x - 50, y + 50] in enemy or (wp_rushed and rushed_pawn_x == x - 50 and y == 300))):
                self.move_lst.append([x - 50, y + 50])

            # down-right (black moves down the board)
            if(x < 450 and y < 450 and ([x + 50, y + 50] in enemy or (wp_rushed and rushed_pawn_x == x + 50 and y == 300))):
                self.move_lst.append([x + 50, y + 50])

            # down one (normal advancement)
            if(y < 450 and is_empty(x, y + 50)):
                self.move_lst.append([x, y + 50])

            # down two (special advancement)
            if(y == 150 and is_empty(x,200) and is_empty(x,250)):
                self.move_lst.append([x, 250])


        else:

            enemy = black_piece_coord_lst

            # up-left (white moves up the board)
            if(x > 100 and y > 100 and ([x - 50, y - 50] in enemy or (bp_rushed and rushed_pawn_x == x - 50 and y == 250))):
                self.move_lst.append([x - 50, y - 50])

            # up-right (white moves up the board)
            if(x < 450 and y > 100 and ([x + 50, y - 50] in enemy or (bp_rushed and rushed_pawn_x == x + 50 and y == 250))):
                self.move_lst.append([x + 50, y - 50])

            # up one (normal advancement)
            if(y > 100 and is_empty(x, y - 50)):
                self.move_lst.append([x, y - 50])

            # up two (special advancement)
            if(y == 400 and is_empty(x, 350) and is_empty(x, 300)):
                self.move_lst.append([x, 300])


    def set_attack_squares(self):

            self.attack_lst = []
            x = adj_coord(board.coords(self.pawn_top)[0])
            y = adj_coord(board.coords(self.pawn_top)[1])


            if(self.color == "black"):


                # down-left (black moves down the board)
                if(x > 100 and y < 450):
                    self.attack_lst.append([x - 50, y + 50])

                # down-right (black moves down the board)
                if(x < 450 and y < 450):
                    self.attack_lst.append([x + 50, y + 50])

            else:

                # up-left (white moves up the board)
                if(x > 100 and y > 100):
                    self.attack_lst.append([x - 50, y - 50])

                # up-right (black moves down the board)
                if(x < 450 and y > 100):
                    self.attack_lst.append([x + 50, y - 50])



# Creates a knight. (x,y) are the top-left coordinates of the square
class knight:

    global board
    global white_piece_coord_lst
    global black_piece_coord_lst

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "knight"

        self.move_lst = []
        self.attack_lst = []


        # The Head
        self.head = board.create_rectangle(x+16, y+10, x+34, y+20, fill = color, outline = color)

        # The Body
        self.body = board.create_rectangle(x+25, y+20, x+34, y+35, fill = color, outline = color)

        # The Base
        self.base = board.create_rectangle(x+16, y+35, x+34, y+45, fill = color, outline = color)

        # The Ears
        self.ears = board.create_polygon(x+33, y+10, x+30, y+5, x+27, y+10, x+24, y+5, x+21, y+10, fill = color, outline = color)

        # The Eyes
        self.eyes = board.create_rectangle(x+26, y+12, x+28 , y+14, fill = "white", outline = "white")


        self.widget_lst = [self.eyes, self.ears, self.base, self.body, self.head]

        self.dummy_x = dummy_convert(self.x)
        self.dummy_y = dummy_convert(self.y)

        # The Head
        self.dummy_head = board.create_rectangle(self.dummy_x + 500+16, self.dummy_y+10, self.dummy_x + 500+34, self.dummy_y+20, fill = color, outline = color)

        # The Body
        self.dummy_body = board.create_rectangle(self.dummy_x + 500+25, self.dummy_y+20, self.dummy_x + 500+34, self.dummy_y+35, fill = color, outline = color)

        # The Base
        self.dummy_base = board.create_rectangle(self.dummy_x + 500+16, self.dummy_y+35, self.dummy_x + 500+34, self.dummy_y+45, fill = color, outline = color)

        # The Ears
        self.dummy_ears = board.create_polygon(self.dummy_x + 500+33, self.dummy_y+10, self.dummy_x + 500+30, self.dummy_y+5, self.dummy_x + 500+27, self.dummy_y+10, self.dummy_x + 500+24, self.dummy_y+5, self.dummy_x + 500+21, self.dummy_y+10, fill = color, outline = color)

        # The Eyes
        self.dummy_eyes = board.create_rectangle(self.dummy_x + 500+26, self.dummy_y+12, self.dummy_x + 500+28 , self.dummy_y+14, fill = "white", outline = "white")


        self.dummy_lst = [self.dummy_eyes, self.dummy_ears, self.dummy_base, self.dummy_body, self.dummy_head]


    def get_x(self):
        current_x = adj_coord(board.coords(self.head)[0])
        return current_x

    def get_y(self):
        current_y = adj_coord(board.coords(self.head)[1])
        return current_y


    def set_move_squares(self):

        if(self.color == "black"):
            piece_coord_lst = black_piece_coord_lst

        else:
            piece_coord_lst = white_piece_coord_lst


        self.move_lst = []
        x = adj_coord(board.coords(self.head)[0])
        y = adj_coord(board.coords(self.head)[1])

        # top-left
        if(x > 100 and y > 150):
            self.move_lst.append([x-50, y-100])

        # top-right
        if(x < 450 and y > 150):
            self.move_lst.append([x + 50, y - 100])

        #bottom-left
        if(x > 100 and y < 400):
            self.move_lst.append([x - 50, y + 100])

        #bottom-right
        if(x < 450 and y < 400):
            self.move_lst.append([x + 50, y + 100])

        #left-up
        if(x > 150 and y > 100):
            self.move_lst.append([x - 100, y - 50])

        #left-down
        if(x > 150 and y < 450):
            self.move_lst.append([x - 100, y + 50])

        #right-up
        if(x < 400 and y > 100):
            self.move_lst.append([x + 100, y - 50])

        #right-down
        if(x < 400 and y < 450):
            self.move_lst.append([x + 100, y + 50])

        for taken_squares in piece_coord_lst:
            if(taken_squares in self.move_lst):
                self.move_lst.remove(taken_squares)


    def set_attack_squares(self):

        self.attack_lst = []
        x = adj_coord(board.coords(self.head)[0])
        y = adj_coord(board.coords(self.head)[1])

        # top-left
        if(x > 100 and y > 150):
            self.attack_lst.append([x-50, y-100])

        # top-right
        if(x < 450 and y > 150):
            self.attack_lst.append([x + 50, y - 100])

        #bottom-left
        if(x > 100 and y < 400):
            self.attack_lst.append([x - 50, y + 100])

        #bottom-right
        if(x < 450 and y < 400):
            self.attack_lst.append([x + 50, y + 100])

        #left-up
        if(x > 150 and y > 100):
            self.attack_lst.append([x - 100, y - 50])

        #left-down
        if(x > 150 and y < 450):
            self.attack_lst.append([x - 100, y + 50])

        #right-up
        if(x < 400 and y > 100):
            self.attack_lst.append([x + 100, y - 50])

        #right-down
        if(x < 400 and y < 450):
            self.attack_lst.append([x + 100, y + 50])



# Creates a bishop. (x,y) are the top-left coordinates of the square
class bishop:

    global board
    global white_piece_coord_lst
    global black_piece_coord_lst

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "bishop"

        self.move_lst = []
        self.attack_lst = []

        # Draws the base
        self.head = board.create_oval(x+16,y+10,x+34,y+30, fill = color, outline = color)
        self.base = board.create_rectangle(x+10, y+40, x+40, y+45, fill = color, outline = color)
        self.stem = board.create_rectangle(x+20, y+29, x+30, y+40, fill = color, outline = color)

        #This is the tiny dot at the top
        self.top = board.create_oval(x+22,y+5,x+28,y+11, fill = color, outline = color)

        # Draws the cross on the goofy hat
        self.vert_cross = board.create_line(x+25,y+14,x+25,y+22, fill = "white")
        self.horz_cross = board.create_line(x+21,y+18,x+29,y+18, fill = "white")

        self.widget_lst = [self.head, self.base, self.stem, self.top, self.vert_cross, self.horz_cross]
        
        
        self.dummy_x = dummy_convert(self.x) + 500
        self.dummy_y = dummy_convert(self.y)
        
        
        # Draws the base
        self.dummy_head = board.create_oval(self.dummy_x+16,self.dummy_y+10,self.dummy_x+34,self.dummy_y+30, fill = color, outline = color)
        self.dummy_base = board.create_rectangle(self.dummy_x+10,self.dummy_y+40, self.dummy_x+40,self.dummy_y+45, fill = color, outline = color)
        self.dummy_stem = board.create_rectangle(self.dummy_x+20,self.dummy_y+29, self.dummy_x+30,self.dummy_y+40, fill = color, outline = color)

        #This is the tiny dot at the top
        self.dummy_top = board.create_oval(self.dummy_x+22,self.dummy_y+5,self.dummy_x+28,self.dummy_y+11, fill = color, outline = color)

        # Draws the cross on the goofy hat
        self.dummy_vert_cross = board.create_line(self.dummy_x+25,self.dummy_y+14,self.dummy_x+25,self.dummy_y+22, fill = "white")
        self.dummy_horz_cross = board.create_line(self.dummy_x+21,self.dummy_y+18,self.dummy_x+29,self.dummy_y+18, fill = "white")

        self.dummy_lst = [self.dummy_head, self.dummy_base, self.dummy_stem, self.dummy_top, self.dummy_vert_cross, self.dummy_horz_cross]


    def get_x(self):
        current_x = adj_coord(board.coords(self.stem)[0])
        return current_x

    def get_y(self):
        current_y = adj_coord(board.coords(self.stem)[1])
        return current_y


    def set_move_squares(self):

        if(self.color == "black"):

            friendly = black_piece_coord_lst
            enemy = white_piece_coord_lst

        else:

            friendly = white_piece_coord_lst
            enemy = black_piece_coord_lst


        self.move_lst = []
        x = adj_coord(board.coords(self.stem)[0])
        y = adj_coord(board.coords(self.stem)[1])

        # up-left
        for a in range(1,8):

            if(x - (50*a) < 100 or y - (50*a) < 100):
                break

            elif([x - (50*a), y - (50*a)] in friendly):
                break

            elif([x - (50*a), y - (50*a)] in enemy):
                self.move_lst.append([x - (50*a), y - (50*a)])
                break

            else:
                self.move_lst.append([x - (50*a), y - (50*a)])


        # up-right
        for a in range(1,8):

            if(x + (50*a) > 450 or y - (50*a) < 100):
                break

            elif([x + (50*a), y - (50*a)] in friendly):
                break

            elif([x + (50*a), y - (50*a)] in enemy):
                self.move_lst.append([x + (50*a), y - (50*a)])
                break

            else:
                self.move_lst.append([x + (50*a), y - (50*a)])


        # down-left
        for a in range(1,8):

            if(x - (50*a) < 100 or y + (50*a) > 450):
                break

            elif([x - (50*a), y + (50*a)] in friendly):
                break

            elif([x - (50*a), y + (50*a)] in enemy):
                self.move_lst.append([x - (50*a), y + (50*a)])
                break

            else:
                self.move_lst.append([x - (50*a), y + (50*a)])

        # down-right
        for a in range(1,8):

            if(x + (50*a) > 450 or y + (50*a) > 450):
                break

            elif([x + (50*a), y + (50*a)] in friendly):
                break

            elif([x + (50*a), y + (50*a)] in enemy):
                self.move_lst.append([x + (50*a), y + (50*a)])
                break

            else:
                self.move_lst.append([x + (50*a), y + (50*a)])
                

    def set_attack_squares(self):


        self.attack_lst = []

        x = adj_coord(board.coords(self.stem)[0])
        y = adj_coord(board.coords(self.stem)[1])


        if(self.color == "black"):
            rival_king = wk

        else:
            rival_king = bk


        king_pos = [rival_king.get_x(), rival_king.get_y()]


        # up-left
        for a in range(1,8):

            if(x - (50*a) < 100 or y - (50*a) < 100):
                break

            elif(is_empty(x - (50*a), y - (50*a))):
                self.attack_lst.append([x - (50*a), y - (50*a)])

            elif(([x - (50*a), y - (50*a)] == king_pos)):
                self.attack_lst.append([x - (50*a), y - (50*a)])

                if(x - (50*a) - 50 >= 100 and y - (50*a) - 50 >= 100):
                    self.attack_lst.append([x - (50*a) - 50, y - (50*a) - 50])
                break

            else:
                self.attack_lst.append([x - (50*a), y - (50*a)])
                break


        # up-right
        for a in range(1,8):

            if(x + (50*a) > 450 or y - (50*a) < 100):
                break

            elif(is_empty(x + (50*a), y - (50*a))):
                self.attack_lst.append([x + (50*a), y - (50*a)])

            elif(([x + (50*a), y - (50*a)] == king_pos)):
                self.attack_lst.append([x + (50*a), y - (50*a)])

                if(x + (50*a) + 50 <= 450 and y - (50*a) - 50 >= 100):
                    self.attack_lst.append([x + (50*a) + 50, y - (50*a) - 50])
                break

            else:
                self.attack_lst.append([x + (50*a), y - (50*a)])
                break


        # down-left
        for a in range(1,8):

            if(x - (50*a) < 100 or y + (50*a) > 450):
                break

            elif(is_empty(x - (50*a), y + (50*a))):
                self.attack_lst.append([x - (50*a), y + (50*a)])

            elif(([x - (50*a), y + (50*a)] == king_pos)):
                self.attack_lst.append([x - (50*a), y + (50*a)])

                if(x - (50*a) - 50 >= 100 and y + (50*a) + 50 <= 450):
                    self.attack_lst.append([x - (50*a) - 50, y + (50*a) + 50])
                break

            else:
                self.attack_lst.append([x - (50*a), y + (50*a)])
                break


        # down-right
        for a in range(1,8):

            if(x + (50*a) > 450 or y + (50*a) > 450):
                break

            elif(is_empty(x + (50*a), y + (50*a))):
                self.attack_lst.append([x + (50*a), y + (50*a)])

            elif(([x + (50*a), y + (50*a)] == king_pos)):
                self.attack_lst.append([x + (50*a), y + (50*a)])

                if(x + (50*a) + 50 <= 450 and y + (50*a) + 50 <= 450):
                    self.attack_lst.append([x + (50*a) + 50, y + (50*a) + 50])
                break

            else:
                self.attack_lst.append([x + (50*a), y + (50*a)])
                break


                
# Creates a rook. (x,y) are the top-left coordinates of the square
class rook:

    global board

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "rook"

        self.move_lst = []
        self.attack_lst = []

        # draws the three stubs on top of the piece
        self.stub_1 = board.create_rectangle(x+13, y+8, x+18, y+13, fill = color, outline = color)
        self.stub_2 = board.create_rectangle(x+22, y+8, x+28, y+13, fill = color, outline = color)
        self.stub_3 = board.create_rectangle(x+32, y+8, x+37, y+13, fill = color, outline = color)

        # draws the base
        self.crown = board.create_rectangle(x+13, y+13, x+37, y+18, fill = color, outline = color)
        self.stem = board.create_rectangle(x+15, y+13, x+35, y+38, fill = color, outline = color)
        self.base = board.create_rectangle(x+10, y+38, x+40, y+45, fill = color, outline = color)


        self.widget_lst = [self.stub_1, self.stub_2, self.stub_3, self.crown, self.stem, self.base]


        self.dummy_x = dummy_convert(self.x) + 500
        self.dummy_y = dummy_convert(self.y)
        
        # draws the three stubs on top of the piece
        self.dummy_stub_1 = board.create_rectangle(self.dummy_x+13, self.dummy_y+8, self.dummy_x+18, self.dummy_y+13, fill = color, outline = color)
        self.dummy_stub_2 = board.create_rectangle(self.dummy_x+22, self.dummy_y+8, self.dummy_x+28, self.dummy_y+13, fill = color, outline = color)
        self.dummy_stub_3 = board.create_rectangle(self.dummy_x+32, self.dummy_y+8, self.dummy_x+37, self.dummy_y+13, fill = color, outline = color)

        # draws the base
        self.dummy_crown = board.create_rectangle(self.dummy_x+13, self.dummy_y+13, self.dummy_x+37, self.dummy_y+18, fill = color, outline = color)
        self.dummy_stem = board.create_rectangle(self.dummy_x+15, self.dummy_y+13, self.dummy_x+35, self.dummy_y+38, fill = color, outline = color)
        self.dummy_base = board.create_rectangle(self.dummy_x+10, self.dummy_y+38, self.dummy_x+40, self.dummy_y+45, fill = color, outline = color)


        self.dummy_lst = [self.dummy_stub_1, self.dummy_stub_2, self.dummy_stub_3, self.dummy_crown, self.dummy_stem, self.dummy_base]
        
        
    def get_x(self):
        current_x = adj_coord(board.coords(self.crown)[0])
        return current_x

    def get_y(self):
        current_y = adj_coord(board.coords(self.crown)[1])
        return current_y


    def set_move_squares(self):


        if(self.color == "black"):
            friendly = black_piece_coord_lst
            enemy = white_piece_coord_lst

        else:
   
            friendly = white_piece_coord_lst
            enemy = black_piece_coord_lst


        self.move_lst = []
        x = adj_coord(board.coords(self.stem)[0])
        y = adj_coord(board.coords(self.stem)[1])

        # left
        for a in range(1,8):

            if(x - (50*a) < 100):
                break

            elif([x - (50*a), y] in friendly):
                break

            elif([x - (50*a), y] in enemy):
                self.move_lst.append([x - (50*a), y])
                break

            else:
                self.move_lst.append([x - (50*a), y])


        # right
        for a in range(1,8):

            if(x + (50*a) > 450):
                break

            elif([x + (50*a), y] in friendly):
                break

            elif([x + (50*a), y] in enemy):
                self.move_lst.append([x + (50*a), y])
                break

            else:
                self.move_lst.append([x + (50*a), y])


        # up
        for a in range(1,8):

            if(y - (50*a) < 100):
                break

            elif([x, y - (50*a)] in friendly):
                break

            elif([x, y - (50*a)] in enemy):
                self.move_lst.append([x, y - (50*a)])
                break

            else:
                self.move_lst.append([x, y - (50*a)])

        # down
        for a in range(1,8):

            if(y + (50*a) > 450):
                break

            elif([x, y + (50*a)] in friendly):
                break

            elif([x, y + (50*a)] in enemy):
                self.move_lst.append([x, y + (50*a)])
                break

            else:
                self.move_lst.append([x, y + (50*a)])



    def set_attack_squares(self):


        self.attack_lst = []
        x = adj_coord(board.coords(self.stem)[0])
        y = adj_coord(board.coords(self.stem)[1])


        if(self.color == "black"):
            rival_king = wk

        else:
            rival_king = bk

        king_pos = [rival_king.get_x(), rival_king.get_y()]


        # left
        for a in range(1,8):

            if(x - (50*a) < 100):
                break

            elif(is_empty(x - (50*a), y)):
                self.attack_lst.append([x - (50*a), y])

            elif([x - (50*a), y] == king_pos):
                self.attack_lst.append([x - (50*a), y])

                if(x - (50*a) - 50 >= 100):
                    self.attack_lst.append([x - (50*a) - 50, y])
                break

            else:
                self.attack_lst.append([x - (50*a), y])
                break

        # right
        for a in range(1,8):

            if(x + (50*a) > 450):
                break

            elif(is_empty(x + (50*a), y)):
                self.attack_lst.append([x + (50*a), y])

            elif([x + (50*a), y] == king_pos):
                self.attack_lst.append([x + (50*a), y])

                if(x + (50*a) + 50 <= 450):
                    self.attack_lst.append([x + (50*a) + 50, y])
                break

            else:
                self.attack_lst.append([x + (50*a), y])
                break


        # up
        for a in range(1,8):

            if(y - (50*a) < 100):
                break

            elif(is_empty(x, y - (50*a))):
                self.attack_lst.append([x, y - (50*a)])

            elif([x, y - (50*a)] == king_pos):
                self.attack_lst.append([x, y - (50*a)])

                if(y - (50*a) - 50 >= 100):
                    self.attack_lst.append([x, y - (50*a) - 50])
                break

            else:
                self.attack_lst.append([x, y - (50*a)])
                break

        # down
        for a in range(1,8):

            if(y + (50*a) > 450):
                break

            elif(is_empty(x, y + (50*a))):
                self.attack_lst.append([x, y + (50*a)])

            elif([x, y + (50*a)] == king_pos):
                self.attack_lst.append([x, y + (50*a)])

                if(y + (50*a) + 50 <= 450):
                    self.attack_lst.append([x, y + (50*a) + 50])
                break

            else:
                self.attack_lst.append([x, y + (50*a)])
                break


# Creates a queen. (x,y) are the top-left coordinates of the square
# The queen combines the mobility of a rook and bishop,
# So I just copied and pasted the rook and bishop set_attack_square() methods
class queen:

    global board

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "queen"

        self.move_lst = []
        self.attack_lst = []

        # This first polygon is rough... it draws the spikes at the top of the crown
        self.crown = board.create_polygon(x+10,y+38,x+6,y+14,   x+14,y+38, x+15,y+10,    x+20,y+38,x+25,y+8,    x+30,y+38,x+35,y+10,   x+36,y+38,x+44,y+14,
        x+40,y+38, fill = color, outline = color)

        # This draws the base
        self.bump = board.create_oval(x+10,y+30,x+40,y+43, fill = color, outline = color)
        self.base = board.create_rectangle(x+10, y+38, x+40, y+45, fill = color, outline = color)

        # Here are the little orbs at the tips of the spikes
        self.orb_1 = board.create_oval(x+4,y+12,x+8,y+16, fill = color, outline = color)
        self.orb_2 = board.create_oval(x+13,y+8,x+17,y+12, fill = color, outline = color)
        self.orb_3 = board.create_oval(x+23,y+6,x+27,y+10, fill = color, outline = color)
        self.orb_4 = board.create_oval(x+33,y+8,x+37,y+12, fill = color, outline = color)
        self.orb_5 = board.create_oval(x+42,y+12,x+46,y+16, fill = color, outline = color)

        self.widget_lst = [self.crown, self.bump, self.base, self.orb_1, self.orb_2, self.orb_3, self.orb_4, self.orb_5]
    
        
        self.dummy_x = dummy_convert(self.x) + 500
        self.dummy_y = dummy_convert(self.y)
        
        
        # This first polygon is rough... it draws the spikes at the top of the crown
        self.dummy_crown = board.create_polygon(self.dummy_x+10,self.dummy_y+38,self.dummy_x+6,self.dummy_y+14,   self.dummy_x+14,self.dummy_y+38, self.dummy_x+15,self.dummy_y+10,    self.dummy_x+20,self.dummy_y+38,self.dummy_x+25,self.dummy_y+8,    self.dummy_x+30,self.dummy_y+38,self.dummy_x+35,self.dummy_y+10,   self.dummy_x+36,self.dummy_y+38,self.dummy_x+44,self.dummy_y+14,
        self.dummy_x+40,self.dummy_y+38, fill = color, outline = color)

        # This draws the base
        self.dummy_bump = board.create_oval(self.dummy_x+10,self.dummy_y+30,self.dummy_x+40,self.dummy_y+43, fill = color, outline = color)
        self.dummy_base = board.create_rectangle(self.dummy_x+10, self.dummy_y+38, self.dummy_x+40, self.dummy_y+45, fill = color, outline = color)

        # Here are the little orbs at the tips of the spikes
        self.dummy_orb_1 = board.create_oval(self.dummy_x+4,self.dummy_y+12,self.dummy_x+8,self.dummy_y+16, fill = color, outline = color)
        self.dummy_orb_2 = board.create_oval(self.dummy_x+13,self.dummy_y+8,self.dummy_x+17,self.dummy_y+12, fill = color, outline = color)
        self.dummy_orb_3 = board.create_oval(self.dummy_x+23,self.dummy_y+6,self.dummy_x+27,self.dummy_y+10, fill = color, outline = color)
        self.dummy_orb_4 = board.create_oval(self.dummy_x+33,self.dummy_y+8,self.dummy_x+37,self.dummy_y+12, fill = color, outline = color)
        self.dummy_orb_5 = board.create_oval(self.dummy_x+42,self.dummy_y+12,self.dummy_x+46,self.dummy_y+16, fill = color, outline = color)

        self.dummy_lst = [self.dummy_crown, self.dummy_bump, self.dummy_base, self.dummy_orb_1, self.dummy_orb_2, self.dummy_orb_3, self.dummy_orb_4, self.dummy_orb_5]

    def get_x(self):
        current_x = adj_coord(board.coords(self.base)[0])
        return current_x

    def get_y(self):
        current_y = adj_coord(board.coords(self.base)[1])
        return current_y


    def set_move_squares(self):


        if(self.color == "black"):
            friendly = black_piece_coord_lst
            enemy = white_piece_coord_lst


        else:

            friendly = white_piece_coord_lst
            enemy = black_piece_coord_lst


        self.move_lst = []
        x = adj_coord(board.coords(self.bump)[0])
        y = adj_coord(board.coords(self.bump)[1])

        # up-left
        for a in range(1,8):

            if(x - (50*a) < 100 or y - (50*a) < 100):
                break

            elif([x - (50*a), y - (50*a)] in friendly):
                break

            elif([x - (50*a), y - (50*a)] in enemy):
                self.move_lst.append([x - (50*a), y - (50*a)])
                break

            else:
                self.move_lst.append([x - (50*a), y - (50*a)])


        # up-right
        for a in range(1,8):

            if(x + (50*a) > 450 or y - (50*a) < 100):
                break

            elif([x + (50*a), y - (50*a)] in friendly):
                break

            elif([x + (50*a), y - (50*a)] in enemy):
                self.move_lst.append([x + (50*a), y - (50*a)])
                break

            else:
                self.move_lst.append([x + (50*a), y - (50*a)])


        # down-left
        for a in range(1,8):

            if(x - (50*a) < 100 or y + (50*a) > 450):
                break

            elif([x - (50*a), y + (50*a)] in friendly):
                break

            elif([x - (50*a), y + (50*a)] in enemy):
                self.move_lst.append([x - (50*a), y + (50*a)])
                break

            else:
                self.move_lst.append([x - (50*a), y + (50*a)])

        # down-right
        for a in range(1,8):

            if(x + (50*a) > 450 or y + (50*a) > 450):
                break

            elif([x + (50*a), y + (50*a)] in friendly):
                break

            elif([x + (50*a), y + (50*a)] in enemy):
                self.move_lst.append([x + (50*a), y + (50*a)])
                break

            else:
                self.move_lst.append([x + (50*a), y + (50*a)])


        # left
        for a in range(1,8):

            if(x - (50*a) < 100):
                break

            elif([x - (50*a), y] in friendly):
                break

            elif([x - (50*a), y] in enemy):
                self.move_lst.append([x - (50*a), y])
                break

            else:
                self.move_lst.append([x - (50*a), y])


        # right
        for a in range(1,8):

            if(x + (50*a) > 450):
                break

            elif([x + (50*a), y] in friendly):
                break

            elif([x + (50*a), y] in enemy):
                self.move_lst.append([x + (50*a), y])
                break

            else:
                self.move_lst.append([x + (50*a), y])


        # up
        for a in range(1,8):

            if(y - (50*a) < 100):
                break

            elif([x, y - (50*a)] in friendly):
                break

            elif([x, y - (50*a)] in enemy):
                self.move_lst.append([x, y - (50*a)])
                break

            else:
                self.move_lst.append([x, y - (50*a)])

        # down
        for a in range(1,8):

            if(y + (50*a) > 450):
                break

            elif([x, y + (50*a)] in friendly):
                break

            elif([x, y + (50*a)] in enemy):
                self.move_lst.append([x, y + (50*a)])
                break

            else:
                self.move_lst.append([x, y + (50*a)])



    def set_attack_squares(self):


        self.attack_lst = []

        x = adj_coord(board.coords(self.bump)[0])
        y = adj_coord(board.coords(self.bump)[1])

        if(self.color == "black"):
            rival_king = wk

        else:
            rival_king = bk


        king_pos = [rival_king.get_x(), rival_king.get_y()]


        # up-left
        for a in range(1,8):

            if(x - (50*a) < 100 or y - (50*a) < 100):
                break

            elif(is_empty(x - (50*a), y - (50*a))):
                self.attack_lst.append([x - (50*a), y - (50*a)])

            elif(([x - (50*a), y - (50*a)] == king_pos)):
                self.attack_lst.append([x - (50*a), y - (50*a)])

                if(x - (50*a) - 50 >= 100 and y - (50*a) - 50 >= 100):
                    self.attack_lst.append([x - (50*a) - 50, y - (50*a) - 50])
                break

            else:
                self.attack_lst.append([x - (50*a), y - (50*a)])
                break


        # up-right
        for a in range(1,8):

            if(x + (50*a) > 450 or y - (50*a) < 100):
                break

            elif(is_empty(x + (50*a), y - (50*a))):
                self.attack_lst.append([x + (50*a), y - (50*a)])

            elif(([x + (50*a), y - (50*a)] == king_pos)):
                self.attack_lst.append([x + (50*a), y - (50*a)])

                if(x + (50*a) + 50 <= 450 and y - (50*a) - 50 >= 100):
                    self.attack_lst.append([x + (50*a) + 50, y - (50*a) - 50])
                break

            else:
                self.attack_lst.append([x + (50*a), y - (50*a)])
                break


        # down-left
        for a in range(1,8):

            if(x - (50*a) < 100 or y + (50*a) > 450):
                break

            elif(is_empty(x - (50*a), y + (50*a))):
                self.attack_lst.append([x - (50*a), y + (50*a)])

            elif(([x - (50*a), y + (50*a)] == king_pos)):
                self.attack_lst.append([x - (50*a), y + (50*a)])

                if(x - (50*a) - 50 >= 100 and y + (50*a) + 50 <= 450):
                    self.attack_lst.append([x - (50*a) - 50, y + (50*a) + 50])
                break

            else:
                self.attack_lst.append([x - (50*a), y + (50*a)])
                break


        # down-right
        for a in range(1,8):

            if(x + (50*a) > 450 or y + (50*a) > 450):
                break

            elif(is_empty(x + (50*a), y + (50*a))):
                self.attack_lst.append([x + (50*a), y + (50*a)])

            elif(([x + (50*a), y + (50*a)] == king_pos)):
                self.attack_lst.append([x + (50*a), y + (50*a)])

                if(x + (50*a) + 50 <= 450 and y + (50*a) + 50 <= 450):
                    self.attack_lst.append([x + (50*a) + 50, y + (50*a) + 50])
                break

            else:
                self.attack_lst.append([x + (50*a), y + (50*a)])
                break

        # left
        for a in range(1,8):

            if(x - (50*a) < 100):
                break

            elif(is_empty(x - (50*a), y)):
                self.attack_lst.append([x - (50*a), y])

            elif([x - (50*a), y] == king_pos):
                self.attack_lst.append([x - (50*a), y])

                if(x - (50*a) - 50 >= 100):
                    self.attack_lst.append([x - (50*a) - 50, y])
                break

            else:
                self.attack_lst.append([x - (50*a), y])
                break

        # right
        for a in range(1,8):

            if(x + (50*a) > 450):
                break

            elif(is_empty(x + (50*a), y)):
                self.attack_lst.append([x + (50*a), y])

            elif([x + (50*a), y] == king_pos):
                self.attack_lst.append([x + (50*a), y])

                if(x + (50*a) + 50 <= 450):
                    self.attack_lst.append([x + (50*a) + 50, y])
                break

            else:
                self.attack_lst.append([x + (50*a), y])
                break


        # up
        for a in range(1,8):

            if(y - (50*a) < 100):
                break

            elif(is_empty(x, y - (50*a))):
                self.attack_lst.append([x, y - (50*a)])

            elif([x, y - (50*a)] == king_pos):
                self.attack_lst.append([x, y - (50*a)])

                if(y - (50*a) - 50 >= 100):
                    self.attack_lst.append([x, y - (50*a) - 50])
                break

            else:
                self.attack_lst.append([x, y - (50*a)])
                break

        # down
        for a in range(1,8):

            if(y + (50*a) > 450):
                break

            elif(is_empty(x, y + (50*a))):
                self.attack_lst.append([x, y + (50*a)])

            elif([x, y + (50*a)] == king_pos):
                self.attack_lst.append([x, y + (50*a)])

                if(y + (50*a) + 50 <= 450):
                    self.attack_lst.append([x, y + (50*a) + 50])
                break

            else:
                self.attack_lst.append([x, y + (50*a)])
                break


# Creates a king. (x,y) are the top-left coordinates of the square
class king:

    global board
    global wk_moved
    global war_moved
    global whr_moved
    global black_attack_lst
    global bk_moved
    global bar_moved
    global bhr_moved
    global white_attack_lst

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "king"

        self.move_lst = []
        self.attack_lst = []

        # This draws the base
        self.bump = board.create_oval(x+10,y+30,x+40,y+43, fill = color, outline = color)
        self.base = board.create_rectangle(x+10, y+38, x+40, y+45, fill = color, outline = color)

        # This draws the stem
        self.stem = board.create_rectangle(x+20, y+22, x+30, y+30, fill = color, outline = color)

        # Draw the crown
        self.cup = board.create_arc(x+15, y+10, x+35, y+22, start = 180, extent = 180, fill = color, outline = color)
        self.vert_cross = board.create_rectangle(x+24, y+4, x+27, y+22, fill = color, outline = color)
        self.horz_cross = board.create_rectangle(x+20, y+8, x+31, y+11, fill = color, outline = color)

        self.widget_lst = [self.bump, self.base, self.stem, self.cup, self.vert_cross, self.horz_cross]
        
        
        self.dummy_x = dummy_convert(self.x) + 500
        self.dummy_y = dummy_convert(self.y)
        
        
        # This draws the base
        self.dummy_bump = board.create_oval(self.dummy_x+10,self.dummy_y+30,self.dummy_x+40,self.dummy_y+43, fill = color, outline = color)
        self.dummy_base = board.create_rectangle(self.dummy_x+10, self.dummy_y+38, self.dummy_x+40, self.dummy_y+45, fill = color, outline = color)

        # This draws the stem
        self.dummy_stem = board.create_rectangle(self.dummy_x+20, self.dummy_y+22, self.dummy_x+30, self.dummy_y+30, fill = color, outline = color)

        # Draw the crown
        self.dummy_cup = board.create_arc(self.dummy_x+15, self.dummy_y+10, self.dummy_x+35, self.dummy_y+22, start = 180, extent = 180, fill = color, outline = color)
        self.dummy_vert_cross = board.create_rectangle(self.dummy_x+24, self.dummy_y+4, self.dummy_x+27, self.dummy_y+22, fill = color, outline = color)
        self.dummy_horz_cross = board.create_rectangle(self.dummy_x+20, self.dummy_y+8, self.dummy_x+31, self.dummy_y+11, fill = color, outline = color)

        self.dummy_lst = [self.dummy_bump, self.dummy_base, self.dummy_stem, self.dummy_cup, self.dummy_vert_cross, self.dummy_horz_cross]
        


    def get_x(self):
        current_x = adj_coord(board.coords(self.stem)[0])
        return current_x

    def get_y(self):
        current_y = adj_coord(board.coords(self.stem)[1])
        return current_y

    def set_move_squares(self):

        self.move_lst = []
        x = adj_coord(board.coords(self.bump)[0])
        y = adj_coord(board.coords(self.bump)[1])

        # top-left
        if(x > 100 and y > 100):
            self.move_lst.append([x - 50, y - 50])

        # up
        if(y > 100):
            self.move_lst.append([x, y - 50])

        # top-right
        if(x < 450 and y > 100):
            self.move_lst.append([x + 50, y - 50])

        # left
        if(x > 100):
            self.move_lst.append([x - 50, y])

        # right
        if(x < 450):
            self.move_lst.append([x + 50, y])

        # bottom-left
        if(x > 100 and y < 450):
            self.move_lst.append([x - 50, y + 50])

        # down
        if(y < 450):
            self.move_lst.append([x, y + 50])

        # bottom-right
        if(x < 450 and y < 450):
            self.move_lst.append([x + 50, y + 50])


        if(self.color == "black"):

            friend = black_piece_coord_lst
            enemy = white_attack_lst

            # queenside castle (black)
            # Need to avoid illegally castling into, out of, or through check
            if(not bk_moved and not bar_moved and [300,100] not in enemy and [250,100] not in enemy and [200,100] not in enemy and is_empty(150,100) and is_empty(200,100) and is_empty(250,100)):
                self.move_lst.append([200,100])

            # kingside castle
            if(not bk_moved and not bhr_moved and [300, 100] not in enemy and [350,100] not in enemy and [400,100] not in enemy and is_empty(350,100) and is_empty(400,100)):
                self.move_lst.append([400,100])

        else:
            friend = white_piece_coord_lst
            enemy = black_attack_lst

            # queenside castle (white)
            # Need to avoid illegally castling into, out of, or through check
            if(not wk_moved and not war_moved and [300,450] not in enemy and [250,450] not in enemy and [200,450] not in enemy and is_empty(150,450) and is_empty(200,450) and is_empty(250,450)):
                self.move_lst.append([200,450])

            # kingside castle
            if(not wk_moved and not whr_moved and [300,450] not in enemy and [350,450] not in enemy and [400,450] not in enemy and is_empty(350,450) and is_empty(400,450)):
                self.move_lst.append([400,450])


        for taken_squares in friend:
            if(taken_squares in self.move_lst):
                self.move_lst.remove(taken_squares)

        for square in enemy:
            if(square in self.move_lst):
                self.move_lst.remove(square)


    def set_attack_squares(self):

        self.attack_lst = []
        x = adj_coord(board.coords(self.bump)[0])
        y = adj_coord(board.coords(self.bump)[1])


        # top-left
        if(x > 100 and y > 100):
            self.attack_lst.append([x - 50, y - 50])

        # up
        if(y > 100):
            self.attack_lst.append([x, y - 50])

        # top-right
        if(x < 450 and y > 100):
            self.attack_lst.append([x + 50, y - 50])

        # left
        if(x > 100):
            self.attack_lst.append([x - 50, y])

        # right
        if(x < 450):
            self.attack_lst.append([x + 50, y])

        # bottom-left
        if(x > 100 and y < 450):
            self.attack_lst.append([x - 50, y + 50])

        # down
        if(y < 450):
            self.attack_lst.append([x, y + 50])

        # bottom-right
        if(x < 450 and y < 450):
            self.attack_lst.append([x + 50, y + 50])


# DELETE (not destroy) a captured piece
# tl;dr I HATE the destroy function (it doesn't work)
def smash_piece(piece):
    for parts in piece.widget_lst:
        board.delete(parts)

def smash_dummy_piece(piece):
    for parts in piece.dummy_lst:
        board.delete(parts)


def in_check(color):

    # black in check
    if(color == "black"):

        king_x = bk.get_x()
        king_y = bk.get_y()
        enemy = white_piece_lst
        friend = black_piece_lst
        double = black_in_double_check

    # white in check
    else:
        king_x = wk.get_x()
        king_y = wk.get_y()
        enemy = black_piece_lst
        friend = white_piece_lst
        double = white_in_double_check



    total_attackers = 0
    attacker = None

    for piece in enemy:
        for square in piece.attack_lst:
            if(square[0] == king_x and square[1] == king_y):
                total_attackers += 1
                attacker = piece


    if(total_attackers > 1):
        double = True
        for defender in friend:
            if(defender.type != "king"):
                defender.move_lst = []



    attack_x = attacker.get_x()
    attack_y = attacker.get_y()


    if(total_attackers == 1):

        if(attacker.type == "pawn" or attacker.type == "knight"):
            for defender in friend:
                if(defender.type != "king"):
                    if([attack_x, attack_y] not in defender.move_lst):
                        defender.move_lst = []

                    else:
                        defender.move_lst = [[attack_x, attack_y]]


        elif(attacker.type == "bishop" or (attacker.type == "queen" and abs(attack_x - king_x) == abs(attack_y - king_y))):

            diag_lst = [[attack_x, attack_y]]




            # from the upper-left
            if(attack_x < king_x and attack_y < king_y):

                distance = int((king_x - attack_x)/50)

                for x in range(1, distance):
                    diag_lst.append([attack_x + (50*x), attack_y + (50*x)])


           # from the upper-right
            elif(attack_x > king_x and attack_y < king_y):

                distance = int((attack_x - king_x)/50)

                for x in range(1, distance):
                    diag_lst.append([attack_x - (50*x), attack_y + (50*x)])


            # from the lower-left
            elif(attack_x < king_x and attack_y > king_y):

                distance = int((king_x - attack_x)/50)

                for x in range(1, distance):
                    diag_lst.append([attack_x + (50*x), attack_y - (50*x)])


            # from the lower-right
            else:

                distance = int((attack_x - king_x)/50)

                for x in range(1, distance):
                    diag_lst.append([attack_x - (50*x), attack_y - (50*x)])


            for defender in friend:
                if(defender.type != "king"):
                    defender.move_lst[:] = [square for square in defender.move_lst if(square in diag_lst)]



        else:

            rook_lst = [[attack_x, attack_y]]

            # from the left
            if(attack_x < king_x):

                distance = int((king_x - attack_x)/50)

                for x in range(1, distance):
                    rook_lst.append([attack_x + (50*x), attack_y])


            # from the right
            elif(attack_x > king_x):

                distance = int((attack_x - king_x)/50)

                for x in range(1, distance):
                    rook_lst.append([attack_x - (50*x), attack_y])


            # from above
            elif(attack_y < king_y):

                distance = int((king_y - attack_y)/50)

                for y in range(1, distance):
                    rook_lst.append([attack_x, attack_y + (50*y)])


            # from below
            else:

                distance = int((attack_y - king_y)/50)

                for y in range(1, distance):
                    rook_lst.append([attack_x, attack_y - (50*y)])

            for defender in friend:
                if(defender.type != "king"):
                    defender.move_lst[:] = [square for square in defender.move_lst if(square in rook_lst)]



# Restricts the movement of a pinned piece... this took forever but it's done now
def is_pinned(color):

    global black_piece_lst
    global white_piece_lst
    global black_piece_coord_lst
    global white_piece_coord_lst
    global wk
    global bk

    if(color == "white"):

        king_x = wk.get_x()
        king_y = wk.get_y()
        attackers = black_piece_lst
        defenders = white_piece_lst
        friend = black_piece_coord_lst
        enemy = white_piece_coord_lst

    else:
        king_x = bk.get_x()
        king_y = bk.get_y()
        attackers = white_piece_lst
        defenders = black_piece_lst
        friend = white_piece_coord_lst
        enemy = black_piece_coord_lst

    # attack from above or below (visually, white moves up the board, black moves down)
    for attacker in attackers:

        if((attacker.type == "rook" or attacker.type == "queen") and attacker.get_x() == king_x and abs(attacker.get_y() - king_y) > 50):

            attack_y = attacker.get_y()

            # from above
            if(attack_y < king_y):

                distance = int((king_y - attack_y)/50)

                count = 0
                pinned_y = 0
                pinned_piece = None

                for y in range(1, distance):

                    if([king_x, attack_y + (50*y)] in friend or count > 1):
                        count = 0
                        break

                    elif([king_x, attack_y + (50*y)] in enemy):
                        count += 1
                        pinned_y = attack_y + (50*y)

                    else:
                        continue

                if(count == 1):
                    for piece in defenders:
                        if(piece.get_x() == king_x and piece.get_y() == pinned_y):
                            pinned_piece = piece
                            break

                    pinned_piece.move_lst[:] = [square for square in pinned_piece.move_lst if(square[0] == king_x)]


            # from below
            else:

                distance = int((attack_y - king_y)/50)

                count = 0
                pinned_y = 0
                pinned_piece = None

                for y in range(1, distance):

                    if([king_x, attack_y - (50*y)] in friend or count > 1):
                        count = 0
                        break

                    elif([king_x, attack_y - (50*y)] in enemy):
                        count += 1
                        pinned_y = attack_y - (50*y)

                    else:
                        continue


                if(count == 1):

                    for piece in defenders:
                        if(piece.get_x() == king_x and piece.get_y() == pinned_y):
                            pinned_piece = piece
                            break

                    pinned_piece.move_lst[:] = [square for square in pinned_piece.move_lst if(square[0] == king_x)]



        if((attacker.type == "rook" or attacker.type == "queen") and attacker.get_y() == king_y and abs(attacker.get_x() - king_x) > 50):

            attack_x = attacker.get_x()

            # from the left
            if(attack_x < king_x):

                distance = int((king_x - attack_x)/50)

                count = 0
                pinned_x = 0
                pinned_piece = None

                for x in range(1, distance):

                    if([attack_x + (50*x), king_y] in friend or count > 1):
                        count = 0
                        break

                    elif([attack_x + (50*x), king_y] in enemy):
                        count += 1
                        pinned_x = attack_x + (50*x)

                    else:
                        continue

                if(count == 1):
                    for piece in defenders:
                        if(piece.get_x() == pinned_x and piece.get_y() == king_y):
                            pinned_piece = piece
                            break

                    pinned_piece.move_lst[:] = [square for square in pinned_piece.move_lst if(square[1] == king_y)]


            # from the right
            else:

                distance = int((attack_x - king_x)/50)

                count = 0
                pinned_x = 0
                pinned_piece = None

                for x in range(1, distance):

                    if([attack_x - (50*x), king_y] in friend or count > 1):
                        count = 0
                        break

                    elif([attack_x - (50*x), king_y] in enemy):
                        count += 1
                        pinned_x = attack_x - (50*x)

                    else:
                        continue


                if(count == 1):

                    for piece in defenders:
                        if(piece.get_x() == pinned_x and piece.get_y() == king_y):
                            pinned_piece = piece
                            break

                    pinned_piece.move_lst[:] = [square for square in pinned_piece.move_lst if(square[1] == king_y)]


        if((attacker.type == "bishop" or attacker.type == "queen") and abs(attacker.get_x() - king_x) == abs(attacker.get_y() - king_y) > 50):

            attack_x = attacker.get_x()
            attack_y = attacker.get_y()

            # from the upper-left
            if(attack_x < king_x and attack_y < king_y):

                distance = int((king_x - attack_x)/50)

                count = 0
                pinned_x = 0
                pinned_y = 0
                diag_lst = [[attack_x, attack_y]]

                pinned_piece = None

                for x in range(1, distance):

                    if([attack_x + (50*x), attack_y + (50*x)] in friend or count > 1):
                        count = 0
                        break

                    elif([attack_x + (50*x), attack_y + (50*x)] in enemy):
                        count += 1
                        pinned_x = attack_x + (50*x)
                        pinned_y = attack_y + (50*x)
                        diag_lst.append([attack_x + (50*x), attack_y + (50*x)])

                    else:
                        diag_lst.append([attack_x + (50*x), attack_y + (50*x)])

                if(count == 1):
                    for piece in defenders:
                        if(piece.get_x() == pinned_x and piece.get_y() == pinned_y):
                            pinned_piece = piece
                            break

                    pinned_piece.move_lst[:] = [square for square in pinned_piece.move_lst if(square in diag_lst)]


           # from the upper-right
            elif(attack_x > king_x and attack_y < king_y):

                distance = int((attack_x - king_x)/50)

                count = 0
                pinned_x = 0
                pinned_y = 0
                diag_lst = [[attack_x, attack_y]]

                pinned_piece = None

                for x in range(1, distance):

                    if([attack_x - (50*x), attack_y + (50*x)] in friend or count > 1):
                        count = 0
                        break

                    elif([attack_x - (50*x), attack_y + (50*x)] in enemy):
                        count += 1
                        pinned_x = attack_x - (50*x)
                        pinned_y = attack_y + (50*x)
                        diag_lst.append([attack_x - (50*x), attack_y + (50*x)])

                    else:
                        diag_lst.append([attack_x - (50*x), attack_y + (50*x)])

                if(count == 1):
                    for piece in defenders:
                        if(piece.get_x() == pinned_x and piece.get_y() == pinned_y):
                            pinned_piece = piece
                            break

                    pinned_piece.move_lst[:] = [square for square in pinned_piece.move_lst if(square in diag_lst)]


            # from the lower-left
            elif(attack_x < king_x and attack_y > king_y):

                distance = int((king_x - attack_x)/50)

                count = 0
                pinned_x = 0
                pinned_y = 0
                diag_lst = [[attack_x, attack_y]]

                pinned_piece = None

                for x in range(1, distance):

                    if([attack_x + (50*x), attack_y - (50*x)] in friend or count > 1):
                        count = 0
                        break

                    elif([attack_x + (50*x), attack_y - (50*x)] in enemy):
                        count += 1
                        pinned_x = attack_x + (50*x)
                        pinned_y = attack_y - (50*x)
                        diag_lst.append([attack_x + (50*x), attack_y - (50*x)])

                    else:
                        diag_lst.append([attack_x + (50*x), attack_y - (50*x)])

                if(count == 1):
                    for piece in defenders:
                        if(piece.get_x() == pinned_x and piece.get_y() == pinned_y):
                            pinned_piece = piece
                            break

                    pinned_piece.move_lst[:] = [square for square in pinned_piece.move_lst if(square in diag_lst)]


            # from the lower-right
            else:

                distance = int((attack_x - king_x)/50)

                count = 0
                pinned_x = 0
                pinned_y = 0
                diag_lst = [[attack_x, attack_y]]

                pinned_piece = None

                for x in range(1, distance):

                    if([attack_x - (50*x), attack_y - (50*x)] in friend or count > 1):
                        count = 0
                        break

                    elif([attack_x - (50*x), attack_y - (50*x)] in enemy):
                        count += 1
                        pinned_x = attack_x - (50*x)
                        pinned_y = attack_y - (50*x)
                        diag_lst.append([attack_x - (50*x), attack_y - (50*x)])

                    else:
                        diag_lst.append([attack_x - (50*x), attack_y - (50*x)])

                if(count == 1):
                    for piece in defenders:
                        if(piece.get_x() == pinned_x and piece.get_y() == pinned_y):
                            pinned_piece = piece
                            break

                    pinned_piece.move_lst[:] = [square for square in pinned_piece.move_lst if(square in diag_lst)]




# Is a square empty?
def is_empty(x,y):

    if([x,y] not in white_piece_coord_lst and [x,y] not in black_piece_coord_lst):
        return True

    else:
        return False

# This method handles A LOT of information that changes after a move
# It switches whose turn it is, resets the master piece, and
def end_move(color):

    global white_to_move
    global master_piece
    global white_attack_lst
    global black_attack_lst
    global white_in_double_check
    global black_in_double_check
    global white_offered_draw
    global black_offered_draw



    if(white_piece_lst == [wk] and len(black_piece_lst) == 2):
            for piece in black_piece_lst:
                if(piece.type == "knight" or piece.type == "bishop"):
                    end_game("black", 0)

    if(black_piece_lst == [bk] and len(white_piece_lst) == 2):
        for piece in white_piece_lst:
            if(piece.type == "knight" or piece.type == "bishop"):
                end_game("white", 0)

    if(color == "black"):

        black_offered_draw = False
        board.itemconfig(black_draw_text, fill = "")

        black_attack_lst = []
        black_in_double_check = False

        for piece in black_piece_lst:
            piece.set_attack_squares()
            for square in piece.attack_lst:
                black_attack_lst.append(square)


        for piece in white_piece_lst:
            piece.set_move_squares()

        # Make it white's move
        white_to_move = True

        # You have to reset the master_piece, otherwise the game would allow you
        # To move that piece over and over with each move_piece event.
        # After the piece moves, the game needs to defer to the mouse again.
        master_piece = None

        is_pinned("white")

        if([wk.get_x(),wk.get_y()] in black_attack_lst):
            in_check("white")

            highlight_check_coords = delta_coords(board.coords(left_red_highlighter)[0], board.coords(left_red_highlighter)[1], wk.get_x(), wk.get_y())
            board.move(left_red_highlighter,highlight_check_coords[0], highlight_check_coords[1])

            highlight_dummy_coords = dummy_delta_coords(board.coords(right_red_highlighter)[0], board.coords(right_red_highlighter)[1], dummy_convert(wk.get_x()) + 500, dummy_convert(wk.get_y()))
            board.move(right_red_highlighter,highlight_dummy_coords[0], highlight_dummy_coords[1])

            board.itemconfig(left_red_highlighter, fill = "orange")
            board.itemconfig(right_red_highlighter, fill = "orange")


        total_pieces = len(white_piece_lst)
        count = 0
        for piece in white_piece_lst:
            if(piece.move_lst == []):
                count += 1

        if(count == total_pieces):
            end_game("white", 1)


    else:

        white_offered_draw = False
        board.itemconfig(white_draw_text, fill = "")

        white_attack_lst = []
        white_in_double_check = False

        for piece in white_piece_lst:
            piece.set_attack_squares()
            for square in piece.attack_lst:
                white_attack_lst.append(square)


        for piece in black_piece_lst:
            piece.set_move_squares()

        # Make it black's move
        white_to_move = False
        master_piece = None


        is_pinned("black")

        if([bk.get_x(),bk.get_y()] in white_attack_lst):
            in_check("black")

            highlight_check_coords = delta_coords(board.coords(left_red_highlighter)[0], board.coords(left_red_highlighter)[1], bk.get_x(), bk.get_y())
            board.move(left_red_highlighter,highlight_check_coords[0], highlight_check_coords[1])

            highlight_dummy_coords = dummy_delta_coords(board.coords(right_red_highlighter)[0], board.coords(right_red_highlighter)[1], dummy_convert(bk.get_x()) + 500, dummy_convert(bk.get_y()))
            board.move(right_red_highlighter,highlight_dummy_coords[0], highlight_dummy_coords[1])

            board.itemconfig(left_red_highlighter, fill = "orange")
            board.itemconfig(right_red_highlighter, fill = "orange")


        total_pieces = len(black_piece_lst)
        count = 0
        for piece in black_piece_lst:
            if(piece.move_lst == []):
                count += 1

        if(count == total_pieces):
            end_game("black", 1)





def end_game(color, mate_num):
    global game_in_progress

    board.itemconfig(left_red_highlighter, fill = "")
    board.itemconfig(right_red_highlighter, fill = "")

    if(mate_num == 0):
        board.create_text(550,50, text = "Draw by Insufficient Material", fill = "black")
        game_in_progress = False


    else:

        if(color == "black"):
            if([bk.get_x(), bk.get_y()] in white_attack_lst):
                board.create_text(550,50, text = "Checkmate: White Wins!", fill = "black")

                for parts in bk.widget_lst:
                    board.itemconfig(parts, fill = "red", outline = "red")

                for parts in bk.dummy_lst:
                    board.itemconfig(parts, fill = "red", outline = "red")

            else:
                board.create_text(550,50, text = "Draw: Stalemate", fill = "black")


        else:
            if([wk.get_x(), wk.get_y()] in black_attack_lst):
                board.create_text(550,50, text = "Checkmate: Black Wins!", fill = "black")
                for parts in wk.widget_lst:
                    board.itemconfig(parts, fill = "red", outline = "red")

                for parts in wk.dummy_lst:
                    board.itemconfig(parts, fill = "red", outline = "red")

            else:
                board.create_text(550,50, text = "Draw: Stalemate", fill = "black")


    small_font = tkFont.Font(family = 'Helvetica', size = 11)

    replay = Button(main, text="Rematch", command = play_again, font = small_font)
    quitt = Button(main, text="Quit", command = quit_game)
    replay.place(x = 550, y = 275, anchor = CENTER)
    quitt.place(x = 550, y = 325, anchor = CENTER)




def promote_piece(key_pressed):

    global master_piece
    global white_to_move
    global promote
    global white_piece_lst
    global black_piece_lst

    if(promote == False):
        return

    elif(white_to_move):
        x = master_piece.get_x()
        y = master_piece.get_y()

        if(key_pressed == "q"):
            new_queen = queen(x, y, "blue")
            white_piece_lst.append(new_queen)

        elif(key_pressed == "r"):
            new_rook = rook(x, y, "blue")
            white_piece_lst.append(new_rook)

        elif(key_pressed == "b"):
            new_bishop = bishop(x, y, "blue")
            white_piece_lst.append(new_bishop)

        elif(key_pressed == "k"):
            new_knight = knight(x, y, "blue")
            white_piece_lst.append(new_knight)

        for parts in master_piece.widget_lst:
            board.delete(parts)

        for parts in master_piece.dummy_lst:
            board.delete(parts)

        white_piece_lst.remove(master_piece)

        board.itemconfig(white_promote_text, fill = "")
        promote = False
        end_move("white")


    else:

        x = master_piece.get_x()
        y = master_piece.get_y()

        if(key_pressed == "q"):
            new_queen = queen(x, y, "black")
            black_piece_lst.append(new_queen)

        elif(key_pressed == "r"):
            new_rook = rook(x, y, "black")
            black_piece_lst.append(new_rook)

        elif(key_pressed == "b"):
            new_bishop = bishop(x, y, "black")
            black_piece_lst.append(new_bishop)

        elif(key_pressed == "k"):
            new_knight = knight(x, y, "black")
            black_piece_lst.append(new_knight)

        for parts in master_piece.widget_lst:
            board.delete(parts)

        for parts in master_piece.dummy_lst:
            board.delete(parts)


        black_piece_lst.remove(master_piece)

        board.itemconfig(black_promote_text, fill = "")
        promote = False
        end_move("black")



# These methods handle promotion: when a pawn reaches the opposite end of the board.
# The player "promotes" the pawn to either a knight, bishop, rook, or queen.
# 99% of the time they're going to pick a queen, but the game needs to account for all options.

# Promote a pawn to a queen
def select_queen(event):

    promote_piece("q")

# Promote to a rook
def select_rook(event):

    promote_piece("r")


# Promote to a bishop.
def select_bishop(event):

   promote_piece("b")


# Promote to a knight.
def select_knight(event):

    promote_piece("k")

#DarkOrange4
# Initializes all the pieces
white_color = "blue"

wap = pawn(100, 400, white_color)
wbp = pawn(150, 400, white_color)
wcp = pawn(200, 400, white_color)
wdp = pawn(250, 400, white_color)
wep = pawn(300, 400, white_color)
wfp = pawn(350, 400, white_color)
wgp = pawn(400, 400, white_color)
whp = pawn(450, 400, white_color)


bap = pawn(100, 150, "black")
bbp = pawn(150, 150, "black")
bcp = pawn(200, 150, "black")
bdp = pawn(250, 150, "black")
bep = pawn(300, 150, "black")
bfp = pawn(350, 150, "black")
bgp = pawn(400, 150, "black")
bhp = pawn(450, 150, "black")


war = rook(100, 450, white_color)
whr = rook(450, 450, white_color)

bar = rook(100, 100, "black")
bhr = rook(450, 100, "black")

wbk = knight(150, 450, white_color)
wgk = knight(400, 450, white_color)

bbk = knight(150, 100, "black")
bgk = knight(400, 100, "black")

wcb = bishop(200, 450, white_color)
wfb = bishop(350, 450, white_color)

bcb = bishop(200, 100, "black")
bfb = bishop(350, 100, "black")

wq = queen(250, 450, white_color)
wk = king(300, 450, white_color)

bq = queen(250, 100, "black")
bk = king(300, 100, "black")



# Adds all the pieces to the black and white piece lists
black_piece_lst = [bap, bbp, bcp, bdp, bep, bfp, bgp, bhp, bar, bhr, bbk, bgk, bcb, bfb, bq, bk]
white_piece_lst = [wap, wbp, wcp, wdp, wep, wfp, wgp, whp, war, whr, wbk, wgk, wcb, wfb, wq, wk]

white_piece_coord_lst = []
for pieces in white_piece_lst:
    white_piece_coord_lst.append([pieces.get_x(), pieces.get_y()])

black_piece_coord_lst = []
for pieces in black_piece_lst:
    black_piece_coord_lst.append([pieces.get_x(), pieces.get_y()])

# This part of the code is super important.
# It sets master_piece (the piece clicked) to None
# It sets white_to_move to true (white moves first)
# It also sets promotion (if a pawn is ready to promote) to "false" which is a necessary condition of click_piece

master_piece = None
white_to_move = True
promote = False
game_in_progress = True
white_offered_draw = False
black_offered_draw = False

# The only purpose of these booleans is to prevent illegal castling
wk_moved = False
bk_moved = False
war_moved = False
whr_moved = False
bar_moved = False
bhr_moved = False

# The only purpose of these booleans is to determine if en passant capturing is legal

wp_rushed = False
bp_rushed = False
rushed_pawn_x = None



# This creates the "selectors" or the icons used to select the destination square for a clicked piece
white_selector = board.create_rectangle(300, 300, 350, 350, width = 7, outline = "blue")
black_selector = board.create_rectangle(750, 300, 800, 350, width = 7, outline = "black")


# These are the move lists... to help with check, checkmate, and stalemate

black_move_lst = []
white_move_lst = []

# These booleans will be useful for handling check
white_in_double_check = False
black_in_double_check = False


# This creates the black and white attack lists, keeping track of all squares attacked by each team
black_attack_lst = []
white_attack_lst = []


for piece in white_piece_lst:
    piece.set_move_squares()

for piece in black_piece_lst:
    piece.set_move_squares()

# Takes target (x,y) and destination (dest_x, dest_y) and works out dx,dy
# The tkinter move function relies on the change (dx,dy) to a coordinate, not the destination coordinate
# I probably could have just used itemconfigure(), but it would take too much work to redo code that already runs fine
def delta_coords(x, y, dest_x, dest_y):

    current_x = adj_coord(x)
    current_y = adj_coord(y)

    dx = abs(dest_x - current_x)
    dy = abs(dest_y - current_y)

    if(current_x > dest_x):
        dx *= -1

    if(current_y > dest_y):
        dy *= -1

    return [dx,dy]


def dummy_delta_coords(x, y, dest_x, dest_y):

    current_x = adj_dummy_coord(x)
    current_y = adj_coord(y)

    dx = abs(dest_x - current_x)
    dy = abs(dest_y - current_y)

    if(current_x > dest_x):
        dx *= -1

    if(current_y > dest_y):
        dy *= -1

    return [dx,dy]



# This method changes the variable master_piece to the piece clicked
# It also highlights the clicked piece with a yellow square
def click_piece(event):

    global white_to_move
    global master_piece
    global white_piece_lst
    global black_piece_lst
    global white_yellow_highlighter
    global black_yellow_highlighter
    global promote
    global game_in_progress


    if(game_in_progress):

        # The if statement makes sure that you clicked inside the board

        if(white_to_move and event.x < 500 and event.x > 100 and event.y < 500 and event.y > 100 and not promote):

            # Hides all previous move squares
            for squares in white_highlight_lst:
                board.itemconfig(squares, fill = "")

            x_corner = adj_coord(event.x)
            y_corner = adj_coord(event.y)

            # Unselects a clicked piece if you click it again
            if(master_piece != None and x_corner == master_piece.get_x() and y_corner == master_piece.get_y()):
                master_piece = None
                board.itemconfig(white_yellow_highlighter, fill = "")
                return


            color = "sky blue"
            piece_lst = white_piece_lst


            for piece in piece_lst:

                if(piece.get_x() == x_corner and piece.get_y() == y_corner):

                    master_piece = piece
                    high_light_coords = delta_coords(board.coords(white_yellow_highlighter)[0], board.coords(white_yellow_highlighter)[1], x_corner, y_corner)
                    board.move(white_yellow_highlighter,high_light_coords[0], high_light_coords[1])
                    board.itemconfig(white_yellow_highlighter, fill = "yellow")

                    for coords in master_piece.move_lst:
                        for squares in white_highlight_lst:

                            if(board.coords(squares)[0] == coords[0] and board.coords(squares)[1] == coords[1]):
                                board.itemconfig(squares, fill = color)

                    return

                master_piece = None
                board.itemconfig(white_yellow_highlighter, fill = "")


        # The if statement makes sure that you clicked inside the board
        if(not white_to_move and event.x < 1000 and event.x > 600 and event.y < 500 and event.y > 100 and not promote):

            # Hides all previous move squares
            for squares in black_highlight_lst:
                board.itemconfig(squares, fill = "")

            x_corner = dummy_convert(adj_coord(event.x - 500))
            y_corner = dummy_convert(adj_coord(event.y))

            # Unselects a clicked piece if you click it again
            if(master_piece != None and x_corner == master_piece.get_x() and y_corner == master_piece.get_y()):
                master_piece = None
                board.itemconfig(black_yellow_highlighter, fill = "")
                return


            color = "Pale green"
            piece_lst = black_piece_lst


            for piece in piece_lst:

                if(piece.get_x() == x_corner and piece.get_y() == y_corner):

                    master_piece = piece
                    high_light_coords = dummy_delta_coords(board.coords(black_yellow_highlighter)[0], board.coords(black_yellow_highlighter)[1], adj_dummy_coord(event.x), adj_coord(event.y))
                    board.move(black_yellow_highlighter,high_light_coords[0], high_light_coords[1])
                    board.itemconfig(black_yellow_highlighter, fill = "yellow")

                    for coords in master_piece.move_lst:
                        for squares in black_highlight_lst:

                            if(board.coords(squares)[0] == dummy_convert(coords[0]) + 500 and board.coords(squares)[1] == dummy_convert(coords[1])):
                                board.itemconfig(squares, fill = color)

                    return

                master_piece = None
                board.itemconfig(black_yellow_highlighter, fill = "")




# If it's white's turn, this method moves the master_piece to the white selector
# after "Return" is pushed
def move_white_piece(event):


    global master_piece
    global white_to_move
    global promote
    global white_piece_coord_lst
    global black_piece_coord_lst
    global whr_moved
    global war_moved
    global wk_moved
    global wp_rushed
    global rushed_pawn_x

    if(master_piece == None or not white_to_move or promote):
        return


    else:

        x_corner = adj_coord(board.coords(white_selector)[0])
        y_corner = adj_coord(board.coords(white_selector)[1])
        current_x = master_piece.get_x()
        current_y = master_piece.get_y()

        if([x_corner, y_corner] not in master_piece.move_lst):
            return


        else:

            board.itemconfig(left_red_highlighter, fill = "")
            board.itemconfig(right_red_highlighter, fill = "")

            wp_rushed = False
            move_lst = delta_coords(current_x, current_y, x_corner, y_corner)

            white_piece_coord_lst.remove([current_x, current_y])
            white_piece_coord_lst.append([x_corner, y_corner])


            if(master_piece.type == "pawn" and move_lst[0] != 0 and [x_corner, y_corner] not in black_piece_coord_lst):
                black_piece_coord_lst.remove([x_corner, y_corner + 50])

                for piece in black_piece_lst:
                    if(piece.get_x() == x_corner and piece.get_y() == y_corner + 50):
                        black_piece_lst.remove(piece)
                        smash_piece(piece)
                        smash_dummy_piece(piece)
                        break


            if([x_corner, y_corner] in black_piece_coord_lst):
                black_piece_coord_lst.remove([x_corner, y_corner])

                for piece in black_piece_lst:
                    if(piece.get_x() == x_corner and piece.get_y() == y_corner):
                        black_piece_lst.remove(piece)
                        smash_piece(piece)
                        smash_dummy_piece(piece)
                        break


            for parts in master_piece.widget_lst:
                board.move(parts, move_lst[0], move_lst[1])

            for parts in master_piece.dummy_lst:
                board.move(parts, -move_lst[0], -move_lst[1])


            board.itemconfig(white_yellow_highlighter, fill = "")

            for squares in white_highlight_lst:
                board.itemconfig(squares, fill = "")


            if(master_piece.type == "pawn" and move_lst[1] == -100):
                wp_rushed = True
                rushed_pawn_x = master_piece.get_x()


            # Prevents illegal castling after rook movement
            if(not war_moved and master_piece == war):
                war_moved = True

            if(not whr_moved and master_piece == whr):
                whr_moved = True

            # Handles castling
            if(not wk_moved and master_piece.type == "king"):

                if(x_corner == 200):

                    for parts in war.widget_lst:
                        board.move(parts, 150, 0)

                    for parts in war.dummy_lst:
                        board.move(parts, -150, 0)

                    white_piece_coord_lst.remove([100,450])
                    white_piece_coord_lst.append([250,450])
                    wk_moved = True
                    end_move("white")
                    return

                elif(x_corner == 400):

                    for parts in whr.widget_lst:
                        board.move(parts, -100, 0)

                    for parts in whr.dummy_lst:
                        board.move(parts, 100, 0)

                    white_piece_coord_lst.remove([450,450])
                    white_piece_coord_lst.append([350,450])
                    wk_moved = True
                    end_move("white")
                    return

                else:
                    wk_moved = True
                    end_move("white")
                    return

            # Hanldes Promotion
            elif(master_piece.get_y() == 100 and master_piece.type == "pawn"):
                promote = True
                board.itemconfig(white_promote_text, fill = "black")
                return

            else:

                end_move("white")



# If it's black's turn, this method moves master_piece to the black selector
# after "space" is pushed
def move_black_piece(event):

    global master_piece
    global white_to_move
    global promote
    global white_piece_coord_lst
    global black_piece_coord_lst
    global bhr_moved
    global bar_moved
    global bk_moved
    global bp_rushed
    global rushed_pawn_x


    if(master_piece == None or white_to_move or promote):

        return

    else:

        board.itemconfig(left_red_highlighter, fill = "")
        board.itemconfig(right_red_highlighter, fill = "")

        dummy_x_corner = adj_dummy_coord(board.coords(black_selector)[0])
        dummy_y_corner = adj_coord(board.coords(black_selector)[1])
        x_corner = dummy_convert(dummy_x_corner - 500)
        y_corner = dummy_convert(dummy_y_corner)


        current_x = master_piece.get_x()
        current_y = master_piece.get_y()


        if([x_corner, y_corner] not in master_piece.move_lst):
            return

        else:

            bp_rushed = False

            move_lst = delta_coords(current_x, current_y, x_corner, y_corner)

            black_piece_coord_lst.remove([current_x, current_y])
            black_piece_coord_lst.append([x_corner, y_corner])

            if(master_piece.type == "pawn" and move_lst[0] != 0 and [x_corner, y_corner] not in white_piece_coord_lst):
                white_piece_coord_lst.remove([x_corner, y_corner - 50])

                for piece in white_piece_lst:
                    if(piece.get_x() == x_corner and piece.get_y() == y_corner - 50):
                        white_piece_lst.remove(piece)
                        smash_piece(piece)
                        smash_dummy_piece(piece)
                        break

            if([x_corner, y_corner] in white_piece_coord_lst):
                white_piece_coord_lst.remove([x_corner, y_corner])
                for piece in white_piece_lst:
                    if(piece.get_x() == x_corner and piece.get_y() == y_corner):
                        white_piece_lst.remove(piece)
                        smash_piece(piece)
                        smash_dummy_piece(piece)
                        break



            for x in master_piece.widget_lst:
                board.move(x, move_lst[0], move_lst[1])

            for x in master_piece.dummy_lst:
                board.move(x, -move_lst[0], -move_lst[1])




            board.itemconfig(black_yellow_highlighter, fill = "")

            for squares in black_highlight_lst:
                board.itemconfig(squares, fill = "")

            if(master_piece.type == "pawn" and move_lst[1] == 100):
                bp_rushed = True
                rushed_pawn_x = master_piece.get_x()

            # Prevents illegal castling after rook movement
            if(not bar_moved and master_piece == bar):
                bar_moved = True

            if(not bhr_moved and master_piece == bhr):
                bhr_moved = True

            # Handles castling
            if(not bk_moved and master_piece.type == "king"):

                if(x_corner == 200):

                    for parts in bar.widget_lst:
                        board.move(parts, 150, 0)

                    for parts in bar.dummy_lst:
                        board.move(parts, -150, 0)

                    black_piece_coord_lst.remove([100, 100])
                    black_piece_coord_lst.append([250, 100])
                    bk_moved = True
                    end_move("black")
                    return

                elif(x_corner == 400):

                    for parts in bhr.widget_lst:
                        board.move(parts, -100, 0)

                    for parts in bhr.dummy_lst:
                        board.move(parts, 100, 0)

                    black_piece_coord_lst.remove([450, 100])
                    black_piece_coord_lst.append([350, 100])
                    bk_moved = True
                    end_move("black")
                    return

                else:
                    bk_moved = True
                    end_move("black")
                    return

            # Handles promotion
            elif(master_piece.get_y() == 450 and master_piece.type == "pawn"):
                promote = True
                board.itemconfig(black_promote_text, fill = "black")
                return

            else:
                end_move("black")


# These methods move the white (blue) player's selector circle around the board
def w_left_key(event):

    if(board.coords(white_selector)[0] > 100):
        board.move(white_selector, -50, 0)

    else:
        board.move(white_selector, 350, 0)

def w_right_key(event):

    if(board.coords(white_selector)[2] < 500):
        board.move(white_selector, 50, 0)

    else:
        board.move(white_selector, -350, 0)

def w_up_key(event):

    if(board.coords(white_selector)[1] > 100):
        board.move(white_selector, 0, -50)

    else:
        board.move(white_selector, 0, 350)

def w_down_key(event):

    if(board.coords(white_selector)[3] < 500):
        board.move(white_selector, 0, 50)

    else:
        board.move(white_selector, 0, -350)


# These methods move the black player's selector square around the board
def b_left_key(event):

    if(board.coords(black_selector)[0] > 600):
        board.move(black_selector, -50, 0)

    else:
        board.move(black_selector, 350, 0)

def b_right_key(event):

    if(board.coords(black_selector)[2] < 1000):
        board.move(black_selector, 50, 0)

    else:
        board.move(black_selector, -350, 0)

def b_up_key(event):

    if(board.coords(black_selector)[1] > 100):
        board.move(black_selector, 0, -50)

    else:
        board.move(black_selector, 0, 350)

def b_down_key(event):

    if(board.coords(black_selector)[3] < 500):
        board.move(black_selector, 0, 50)

    else:
        board.move(black_selector, 0, -350)


def play_again():
    rematch = sys.executable
    os.execl(rematch, rematch, * sys.argv)

def quit_game():
    global main
    main.quit()



# KEY BINDS!!!
main.bind("<Left>", b_left_key)
main.bind("<Right>", b_right_key)
main.bind("<Up>", b_up_key)
main.bind("<Down>", b_down_key)

main.bind("a", w_left_key)
main.bind("d", w_right_key)
main.bind("w", w_up_key)
main.bind("s", w_down_key)


main.bind("q", select_queen)
main.bind("r", select_rook)
main.bind("b", select_bishop)
main.bind("k", select_knight)

main.bind("<space>", move_white_piece)
main.bind("<Return>", move_black_piece)
board.bind("<1>", click_piece)


main.mainloop()
