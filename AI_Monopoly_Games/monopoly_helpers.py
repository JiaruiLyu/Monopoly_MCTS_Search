from Player import *
from BoardCell import *
import random

# global variable
n = 2  # initialize the number of players
grid = random.randint(25, 40) # initialize the number of grids(random from 25 to 40)
playerlist = [] 
boardlist = []
boardIndex = []    
for i in range(grid):
    cell = BoardCell(0, 0, 0, 0, 0, 0)
    boardIndex.append(i) # initilize boardIndex    
    boardlist.append(cell(i)) 

# Return a string representation of num that is always two characters wide.
# Assume num is either one or two digits long.
# If num does not already have two digits, a leading "0" is inserted in front.
# For example, pad(12) is "12", and pad(1) is "01".
def pad(num: int) -> str:

    return str(num).zfill(2) 

def initial_state():

    ### Initialize players ###
    # player = (gold, hp, location)
    # INITIAL: gold: 50, initial hp: 5, intial location: 0
    for i in range(n):
        player = Player(50, 5, 0)
        id = i+1
        playerlist.append(player(id))
        #player.playerForUse()

    ### Initialize Board ###
    # boardcell = ((boxcheck, ruleA, amountA), (playerID, ruleB, amountB))
    # INITIAL: boxcheck=0, ruleA=0, amountA=0, playerID=0, ruleB=0, amountB=0
    for i in range(grid):
        cell = BoardCell(0, 0, 0, 0, 0, 0)
        boardIndex.append(i) # initilize boardIndex    
        boardlist.append(cell(i)) 
    
    #print(boardlist)

#initial_state()     


def drop_lucky_box(board: list) -> list: 
    boxes = random.randint(int(grid/8), int(grid/5)) # initialize the number of lucky boxes (randomly droped)
    #spots = random.sample(boardIndex, boxes)

    print(boxes)
    print(int(grid/8), int(grid/5))


print(boardlist)
#drop_lucky_box(boardlist)

# Return a string representation of the index of all boardcells  
# The string has three indented lines of text.
# The numbers should be padded and evenly spaced.
# If the number of grid is even (eg. 28), the string representation should be like:
# 
#            00 01 02 03 04 05 06 07 08 09 10 11 12
#         27                                        13
#            26 25 24 23 22 21 20 19 18 17 16 15 14
# 
# If the number of grid is odd (eg. 27), the string representation should be like:
# 
#            00 01 02 03 04 05 06 07 08 09 10 11 12
#                                                   13
#            26 25 24 23 22 21 20 19 18 17 16 15 14
# 
# Excluding the leading comment symbols "# " above, all blank space should match exactly:
#   There are exactly 8 blank spaces before the left (padded) number.
#   There is exactly 1 blank space between each (padded) pit number.
#   The returned string should start and end with new-line characters ("\n")
def string_of_boardIndex(board: list) -> str:
   
    # the number of grids is even
    if(grid % 2 == 0):
        edgeline = int(grid/2) # the number of grids in line 1 (= line 3)

        line1 = [pad(i) for i in range(0, edgeline-1, 1)]
        newline1 = " ".join(line1)
        newline1 = '\n           ' + newline1 
        
        line2insert = ' '
        for i in range (0, edgeline - 1):
            line2insert += '   '

        line3 = [pad(i) for i in range(grid-2, edgeline-1, -1)]
        newline3 = " ".join(line3)
        newline3 = '\n           ' + newline3

        outstr = newline1 +'\n        '+ pad(grid-1) + line2insert + pad(edgeline-1)+ newline3+'\n'

    # the number of grids is odd
    else:
        edgeline = int(grid/2 + 1) # the number of grids in line 1 (= line 3)

        line1 = [pad(i) for i in range(0, edgeline-1, 1)]
        newline1 = " ".join(line1)
        newline1 = '\n           ' + newline1 
        
        line2insert = ' '
        for i in range (0, edgeline - 1):
            line2insert += '   '

        line3 = [pad(i) for i in range(grid-1, edgeline-1, -1)]
        newline3 = " ".join(line3)
        newline3 = '\n           ' + newline3

        outstr = newline1 +'\n          '+ line2insert + pad(edgeline-1) + newline3+'\n'

    return outstr
