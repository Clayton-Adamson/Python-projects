
# At first I tried to string my way through this... what a terrible idea

# "White" has blue pieces, black has black.
# Select a piece by clicking it.
# Move a piece using the selector icons.
# White player: arrow keys to move selector, Enter to confirm
# Black player: wasd to move selector, Space to confirm

# Separate move and attack lsts for all pieces


# For 3-fold repetition, make a giant list that appends board postitions with booleans tacked
# onto the end of the list, it shouldn't be hard to make a method that returns [type, x, y], and the giant
# list can be cleared to the current position upon a capture or pawn move
# a separate (but loosely connected) list can increment the count of the position based on the index of the position
# in the giant list


from Tkinter import *


main = Tk()

board = Canvas(main, width = 600, height = 600)
board.pack()


board.create_rectangle(90,90,510,510, fill = "dark grey")
# Draws the edges of the board
board.create_line(100, 100, 500, 100)
board.create_line(100, 100, 100, 500)
board.create_line(500, 100, 500, 500)
board.create_line(100, 500, 500, 500)


# Draws the Rank labels (1-8)
for x in range(0,8):
    board.create_text(65, 126 + x*50, font = "Times 19", text = str(8-x))

# Draws the File labels (A-H)
board.create_text(300, 545, font = "Times 19", text = "A        B        C        D        E        F        G        H")

# Draws invisible text that will prompt the user to press keys for promotion (text will appear when promote = True)
promote_text = board.create_text(300,50, text = "Press Q, R, B, or K to promote to a Queen, Rook, Bishop, or Knight", fill = "")


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

        else:
            #lightgoldenrod2
            board.create_rectangle(100 + 50*x, 100 + 50*y, 150 + 50*x, 150 + 50*y, fill = "white")

# Creates the yellow highlighter square that shows which piece has been clicked
yellow_highlighter = board.create_rectangle(100,100,150,150)
red_highlighter = board.create_rectangle(200,200,250,250)



# Creates the invisible squares that "light up" to show the available attack squares for the clicked piece
highlight_lst = []

def set_highlight_squares():

    for y in range(0,8):
        for x in range(0,8):
            square = board.create_rectangle(100 + 50*x, 100 + 50*y, 150 + 50*x, 150 + 50*y, fill = "")
            highlight_lst.append(square)

set_highlight_squares()

# Method that standardizes any coordinate to a square's top left corner
def adj_coord(raw_num):

    b = 0

    for a in range(1,9):
        if(raw_num < 100 + a*50):
            b = 50 + (a*50)
            return b


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
                self.attack_lst.append([x - (50*a), y - (50*a)])

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
                self.attack_lst.append([x - (50*a), y - (50*a)])

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
                self.attack_lst.append([x - (50*a), y - (50*a)])

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
                self.attack_lst.append([x - (50*a), y - (50*a)])

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
    global bk_moved
    global war_moved
    global whr_moved
    global bar_moved
    global bhr_moved
    global white_attack_lst
    global black_attack_lst

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


# Restricts the movement of a pinned piece... this took forever but it's done now
def is_pinned(color):

    global black_piece_lst
    global white_piece_lst
    global black_piece_coord_lst
    global white_piece_coord_lst
    global wk
    global bk

    if(color == "black"):

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

                    if([king_x, attack_y + (50*y)] in friend):
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

                    if([king_x, attack_y - (50*y)] in friend):
                        count = 2
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

                    if([attack_x + (50*x), king_y] in friend):
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

                    if([attack_x - (50*x), king_y] in friend):
                        count = 2
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

                    if([attack_x + (50*x), attack_y + (50*x)] in friend):
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

    if(color == "black"):

        black_attack_lst = []

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

        is_pinned("black")

    else:

        white_attack_lst = []

        for piece in white_piece_lst:
            piece.set_attack_squares()
            for square in piece.attack_lst:
                white_attack_lst.append(square)


        for piece in black_piece_lst:
            piece.set_move_squares()

        # Make it black's move
        white_to_move = False
        master_piece = None
        is_pinned("white")



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

        white_piece_lst.remove(master_piece)

        board.itemconfig(promote_text, fill = "")
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


        black_piece_lst.remove(master_piece)

        board.itemconfig(promote_text, fill = "")
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
white_selector = board.create_oval(104, 454, 146, 496, width = 7, outline = "blue")
black_selector = board.create_rectangle(100, 100, 150, 150, width = 7, outline = "black")


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



# This method changes the variable master_piece to the piece clicked
# It also highlights the clicked piece with a yellow square
def click_piece(event):

    global white_to_move
    global master_piece
    global white_piece_lst
    global black_piece_lst
    global yellow_highlighter
    global promote



    # The if statement makes sure that you clicked inside the board

    if(event.x < 500 and event.x > 100 and event.y < 500 and event.y > 100 and not promote):

        # Hides all previous move squares
        for squares in highlight_lst:
            board.itemconfig(squares, fill = "")

        x_corner = adj_coord(event.x)
        y_corner = adj_coord(event.y)

        # Unselects a clicked piece if you click it again
        if(master_piece != None and x_corner == master_piece.get_x() and y_corner == master_piece.get_y()):
            master_piece = None
            board.itemconfig(yellow_highlighter, fill = "")
            return

        if(white_to_move):
            color = "sky blue"
            piece_lst = white_piece_lst


        else:
            color = "Pale green"
            piece_lst = black_piece_lst


        for piece in piece_lst:

            if(piece.get_x() == x_corner and piece.get_y() == y_corner):

                master_piece = piece
                high_light_coords = delta_coords(board.coords(yellow_highlighter)[0], board.coords(yellow_highlighter)[1], x_corner, y_corner)
                board.move(yellow_highlighter,high_light_coords[0], high_light_coords[1])
                board.itemconfig(yellow_highlighter, fill = "yellow")

                for coords in master_piece.move_lst:
                    for squares in highlight_lst:

                        if(board.coords(squares)[0] == coords[0] and board.coords(squares)[1] == coords[1]):
                            board.itemconfig(squares, fill = color)

                return

            master_piece = None
            board.itemconfig(yellow_highlighter, fill = "")




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
                        break


            if([x_corner, y_corner] in black_piece_coord_lst):
                black_piece_coord_lst.remove([x_corner, y_corner])

                for piece in black_piece_lst:
                    if(piece.get_x() == x_corner and piece.get_y() == y_corner):
                        black_piece_lst.remove(piece)
                        smash_piece(piece)
                        break

            for parts in master_piece.widget_lst:
                board.move(parts, move_lst[0], move_lst[1])


            board.itemconfig(yellow_highlighter, fill = "")

            for squares in highlight_lst:
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
                    white_piece_coord_lst.remove([100,450])
                    white_piece_coord_lst.append([250,450])
                    wk_moved = True
                    end_move("white")
                    return

                elif(x_corner == 400):

                    for parts in whr.widget_lst:
                        board.move(parts, -100, 0)
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
                board.itemconfig(promote_text, fill = "black")
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

        x_corner = adj_coord(board.coords(black_selector)[0])
        y_corner = adj_coord(board.coords(black_selector)[1])
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
                        break

            if([x_corner, y_corner] in white_piece_coord_lst):
                white_piece_coord_lst.remove([x_corner, y_corner])
                for piece in white_piece_lst:
                    if(piece.get_x() == x_corner and piece.get_y() == y_corner):
                        white_piece_lst.remove(piece)
                        smash_piece(piece)
                        break

            for x in master_piece.widget_lst:
                board.move(x, move_lst[0], move_lst[1])

            board.itemconfig(yellow_highlighter, fill = "")

            for squares in highlight_lst:
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

                    black_piece_coord_lst.remove([100, 100])
                    black_piece_coord_lst.append([250, 100])
                    bk_moved = True
                    end_move("black")
                    return

                elif(x_corner == 400):

                    for parts in bhr.widget_lst:
                        board.move(parts, -100, 0)

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
                board.itemconfig(promote_text, fill = "black")
                return

            else:
                end_move("black")


# These methods move the white (blue) player's selector circle around the board
def w_left_key(event):

    if(board.coords(white_selector)[0] > 104):
        board.move(white_selector, -50, 0)

    else:
        board.move(white_selector, 350, 0)

def w_right_key(event):

    if(board.coords(white_selector)[2] < 496):
        board.move(white_selector, 50, 0)

    else:
        board.move(white_selector, -350, 0)

def w_up_key(event):

    if(board.coords(white_selector)[1] > 104):
        board.move(white_selector, 0, -50)

    else:
        board.move(white_selector, 0, 350)

def w_down_key(event):

    if(board.coords(white_selector)[3] < 496):
        board.move(white_selector, 0, 50)

    else:
        board.move(white_selector, 0, -350)


# These methods move the black player's selector square around the board
def b_left_key(event):

    if(board.coords(black_selector)[0] > 100):
        board.move(black_selector, -50, 0)

    else:
        board.move(black_selector, 350, 0)

def b_right_key(event):

    if(board.coords(black_selector)[2] < 500):
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


# KEY BINDS!!!
main.bind("<Left>", w_left_key)
main.bind("<Right>", w_right_key)
main.bind("<Up>", w_up_key)
main.bind("<Down>", w_down_key)

main.bind("a", b_left_key)
main.bind("d", b_right_key)
main.bind("w", b_up_key)
main.bind("s", b_down_key)


main.bind("q", select_queen)
main.bind("r", select_rook)
main.bind("b", select_bishop)
main.bind("k", select_knight)

main.bind("<space>", move_black_piece)
main.bind("<Return>", move_white_piece)
board.bind("<1>", click_piece)

main.mainloop()
