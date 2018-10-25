
# At first I tried to string my way through this... what a terrible idea

# "White" has blue pieces, black has black.
# Select a piece by clicking it.
# Move a piece using the selector icons.
# White player: arrow keys to move selector, Enter to confirm
# Black player: wasd to move selector, Space to confirm
# I finished pawn promotion, but still have to program all the rules


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
            board.create_rectangle(100 + 50*x, 100 + 50*y, 150 + 50*x, 150 + 50*y, fill = "chocolate")

        else:
            board.create_rectangle(100 + 50*x, 100 + 50*y, 150 + 50*x, 150 + 50*y, fill = "white")

green_highlighter = board.create_rectangle(100,100,150,150)




# These are the piece classes

# Creates a pawn, (x,y) are the top-left coordinates of the square
class pawn:

    global board

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.pawn_top = board.create_oval(x+18,y+11,x+32,y+25, fill = color, outline = color)
        self.pawn_base = board.create_polygon(x+25, y+20, x+35, y+40, x+15, y+40, fill = color, outline = color)
        # issoo beautiful
        self.widget_lst = [self.pawn_top, self.pawn_base]
        self.type = "pawn"


    def get_x(self):
        current_x = adj_coord(board.coords(self.pawn_top)[0])
        return current_x

    def get_y(self):
        current_y = adj_coord(board.coords(self.pawn_top)[1])
        return current_y


# Creates a rook. (x,y) are the top-left coordinates of the square
class rook:

    global board

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "rook"

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

# Creates a knight. (x,y) are the top-left coordinates of the square
class knight:

    global board

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "knight"


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

# Creates a bishop. (x,y) are the top-left coordinates of the square
class bishop:

    global board

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "bishop"

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

# Creates a queen. (x,y) are the top-left coordinates of the square
class queen:

    global board

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "queen"

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


# Creates a king. (x,y) are the top-left coordinates of the square
class king:

    global board

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.type = "king"

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
        white_to_move = False
        master_piece = None
        promote = False


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
        white_to_move = True
        master_piece = None
        promote = False



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


# Initializes all the pieces

wap = pawn(100, 400, "blue")
wbp = pawn(150, 400, "blue")
wcp = pawn(200, 400, "blue")
wdp = pawn(250, 400, "blue")
wep = pawn(300, 400, "blue")
wfp = pawn(350, 400, "blue")
wgp = pawn(400, 400, "blue")
whp = pawn(450, 400, "blue")


bap = pawn(100, 150, "black")
bbp = pawn(150, 150, "black")
bcp = pawn(200, 150, "black")
bdp = pawn(250, 150, "black")
bep = pawn(300, 150, "black")
bfp = pawn(350, 150, "black")
bgp = pawn(400, 150, "black")
bhp = pawn(450, 150, "black")


war = rook(100, 450, "blue")
whr = rook(450, 450, "blue")

bar = rook(100, 100, "black")
bhr = rook(450, 100, "black")

wbk = knight(150, 450, "blue")
wgk = knight(400, 450, "blue")

bbk = knight(150, 100, "black")
bgk = knight(400, 100, "black")

wcb = bishop(200, 450, "blue")
wfb = bishop(350, 450, "blue")

bcb = bishop(200, 100, "black")
bfb = bishop(350, 100, "black")

wq = queen(250, 450, "blue")
wk = king(300, 450, "blue")

bq = queen(250, 100, "black")
bk = king(300, 100, "black")


# Adds all the pieces to the black and white piece lists
black_piece_lst = [bap, bbp, bcp, bdp, bep, bfp, bgp, bhp, bar, bhr, bbk, bgk, bcb, bfb, bq, bk]
white_piece_lst = [wap, wbp, wcp, wdp, wep, wfp, wgp, whp, war, whr, wbk, wgk, wcb, wfb, wq, wk]


# This part of the code is super important.
# It sets master_piece (the piece clicked) to None
# It sets white_to_move to true (white moves first)
# It also sets promotion (if a pawn is ready to promote) to "false" which is a necessary condition of click_piece

master_piece = None
white_to_move = True
promote = False

# This creates the "selectors" or the icons used to select the destination square for a clicked piece
white_selector = board.create_oval(104, 454, 146, 496, width = 7, outline = "blue")
black_selector = board.create_rectangle(100, 100, 150, 150, width = 7, outline = "black")


# Method that standardizes any coordinate to a square's top left corner
def adj_coord(raw_num):

    b = 0

    for a in range(1,9):
        if(raw_num < 100 + a*50):
            b = 50 + (a*50)
            return b


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
# It also highlights the clicked piece with a green square
def click_piece(event):

    global white_to_move
    global master_piece
    global white_piece_lst
    global black_piece_lst
    global green_highlighter
    global promote



    # The if statement makes sure that you clicked inside the board
    if(event.x < 500 and event.x > 100 and event.y < 500 and event.y > 100 and not promote):

        x_corner = adj_coord(event.x)
        y_corner = adj_coord(event.y)


        if(white_to_move):
            for piece in white_piece_lst:

                if(piece.get_x() == x_corner and piece.get_y() == y_corner):

                    master_piece = piece
                    high_light_coords = delta_coords(board.coords(green_highlighter)[0], board.coords(green_highlighter)[1], x_corner, y_corner)
                    board.move(green_highlighter,high_light_coords[0], high_light_coords[1])
                    board.itemconfig(green_highlighter, fill = "green")
                    return

            master_piece = None
            board.itemconfig(green_highlighter, fill = "")



        else:
            for piece in black_piece_lst:
                if(piece.get_x() == x_corner and piece.get_y() == y_corner):

                    master_piece = piece

                    high_light_coords = delta_coords(board.coords(green_highlighter)[0], board.coords(green_highlighter)[1], x_corner, y_corner)
                    board.move(green_highlighter,high_light_coords[0], high_light_coords[1])
                    board.itemconfig(green_highlighter, fill = "green")
                    return

                master_piece = None
                board.itemconfig(green_highlighter, fill = "")


# If it's white's turn, this method moves the master_piece to the white selector
# after "Return" is pushed
def move_white_piece(event):


    global master_piece
    global white_to_move
    global promote

    if(master_piece == None or not white_to_move or promote):
        return


    else:

        x_corner = adj_coord(board.coords(white_selector)[0])
        y_corner = adj_coord(board.coords(white_selector)[1])
        current_x = master_piece.get_x()
        current_y = master_piece.get_y()
        move_lst = delta_coords(current_x, current_y, x_corner, y_corner)

        for x in master_piece.widget_lst:
            board.move(x, move_lst[0], move_lst[1])

        board.itemconfig(green_highlighter, fill = "")

        if(master_piece.get_y() == 100 and master_piece.type == "pawn"):
            promote = True
            board.itemconfig(promote_text, fill = "black")
            return

        else:

            # Make it black's move
            white_to_move = False

            # You have to reset the master_piece, otherwise the game would allow you
            # To move that piece over and over with each move_piece event.
            # After the piece moves, the game needs to defer to the mouse again.
            master_piece = None


# If it's black's turn, this method moves master_piece to the black selector
# after "space" is pushed
def move_black_piece(event):

    global master_piece
    global white_to_move
    global promote

    if(master_piece == None or white_to_move or promote):
        return

    else:

        x_corner = adj_coord(board.coords(black_selector)[0])
        y_corner = adj_coord(board.coords(black_selector)[1])
        current_x = master_piece.get_x()
        current_y = master_piece.get_y()
        move_lst = delta_coords(current_x, current_y, x_corner, y_corner)

        for x in master_piece.widget_lst:
            board.move(x, move_lst[0], move_lst[1])

        board.itemconfig(green_highlighter, fill = "")

        if(master_piece.get_y() == 450 and master_piece.type == "pawn"):
            promote = True
            board.itemconfig(promote_text, fill = "black")
            return

        else:

            # Make it black's move
            white_to_move = True

            # You have to reset the master_piece, otherwise the game would allow you
            # To move that piece over and over with each move_piece event.
            # After the piece moves, the game needs to defer to the mouse again.
            master_piece = None

# These methods move the white (blue) player's selector circle around the board
def w_left_key(event):
    if(board.coords(white_selector)[0] > 104):
        board.move(white_selector, -50, 0)

def w_right_key(event):
    if(board.coords(white_selector)[2] < 496):
        board.move(white_selector, 50, 0)

def w_up_key(event):
    if(board.coords(white_selector)[1] > 104):
        board.move(white_selector, 0, -50)

def w_down_key(event):
    if(board.coords(white_selector)[3] < 496):
        board.move(white_selector, 0, 50)


# These methods move the black player's selector square around the board
def b_left_key(event):
    if(board.coords(black_selector)[0] > 100):
        board.move(black_selector, -50, 0)

def b_right_key(event):
    if(board.coords(black_selector)[2] < 500):
        board.move(black_selector, 50, 0)

def b_up_key(event):
    if(board.coords(black_selector)[1] > 100):
        board.move(black_selector, 0, -50)

def b_down_key(event):
    if(board.coords(black_selector)[3] < 500):
        board.move(black_selector, 0, 50)


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