from Player import *
from BoardCell import *
import random

class Game:
    def __init__(self):
        self.turn = 0

# global variable
n = 2  # initialize the number of players (fixed to be 2)
#grid = random.randint(25, 40) # initialize the number of grids(random from 25 to 40)
grid = 28 # temporary set for test
roundcount = 0 # used to count how many rounds have already passed

# Return a string representation of num that is always two characters wide.
# Assume num is either one or two digits long.
# If num does not already have two digits, a leading "0" is inserted in front.
# For example, pad(12) is "12", and pad(1) is "01".
def pad(num: int) -> str:

    return str(num).zfill(2) 

# Return a list that stores each grid's index
def boardIndex(grids: int) -> list:

    boardIndexlist = []
    for i in range(grids):
        boardIndexlist.append(i) # initilize boardIndex  

    return boardIndexlist  

def initial_state() -> tuple:
    print("Welcome to Monopoly!")

    global grid
    tempgrid = grid

    playerlist = [] 
    boardlist = []

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
    for i in range(tempgrid):
        cell = BoardCell(0, 0, 0, 0, 0, 0)
        boardlist.append(cell(i)) 

    return (playerlist, boardlist)

# Return True if the game is over, and False otherwise.
# The game is over if any user has 0 hp and cant pay the tolls
def game_over(state: tuple) -> bool:
    playerlist = state[0]
    checkhp = 0
    for i in range(len(playerlist)):
        #只要有player是0 hp，不管有多少gold, 直接出局
        if (playerlist[i][1] == 0):
            checkhp = 1

    return bool(checkhp)

def player_nextround_order(roundnum: int) -> tuple:
   
    orderlist = [] #存储的是playerindex，按顺序的
    dicenumlist = []
    dicedict = {}
    sorteddict = []

    if (roundnum == 0):  #roundnum = 0意味着还没开始,则下一轮按index顺序走，比如 0 -> 1 -> 2
        for i in range(n):
            orderlist.append(i)
    else:  #这一轮谁大，下一轮谁先走

        for i in range(n):
            dicenum = random.randint(1, 6)
            dicedict[i] = dicenum

        sorteddict = sorted(dicedict.items(), key=lambda x: x[1], reverse=True)
        for i in range (len(sorteddict)):
            orderlist.append(sorteddict[i][0])
            dicenumlist.append(sorteddict[i][1])

    global roundcount
    roundcount = roundnum+1
    print ((orderlist, dicenumlist))
    return (orderlist, dicenumlist) 

def drop_lucky_box(state: tuple) -> list: 
    global grid
    tempgrid = grid
    
    boxes = random.randint(int(tempgrid/8), int(tempgrid/5)) # initialize the number of lucky boxes (randomly droped)
    
    res = state[1]

    indexList = boardIndex(tempgrid)
    boxSpots = random.sample(indexList, boxes)
    cellList = []
    for i in range(len(boxSpots)):
        cellList = list(res[boxSpots[i]][0])
        cellList[0] = 1
        newCellTuple = tuple(cellList)

        res[boxSpots[i]] = (newCellTuple, res[boxSpots[i]][1])

    return res

def move_one_round(playerOrder: tuple, state: tuple) -> tuple:

    playerlist = state[0]
    boardlist = state[1]

    ind = playerOrder[0]
    addup = playerOrder[1]

    for i in range(n):   
        pList = list(playerlist[ind[i]])
        temp = pList[2] + addup[i]
        pList[2] = temp % grid
        newpTuple = tuple(pList)
        playerlist[ind[i]] = newpTuple 
        pList = []
 
    return (playerlist, boardlist)

# v = player_nextround_order(1)
# s = ([(50, 5, 0), (50, 5, 0)], [((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0))])
# move_one_round(v, s)

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
