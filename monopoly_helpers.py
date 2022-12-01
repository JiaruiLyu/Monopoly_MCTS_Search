from Player import *
from BoardCell import *
import random

### global variable ###
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

# Player has to use gold to occupy the grid, each grid's value is randomly generated from 10 to 18
# The tolls value of each grid will be equal to 1/3 of the grid value
def board_grid_value(grids: int) -> tuple:
    gridIndex = [] # a list stores each grid's index
    gridValue = [] # a list stores each grid's value
    gridToll = [] # a list stores the amount of tolls that needs to be paid for the player who arrived here(if the grid is occupied)

    for i in range(grids):
        value = random.randint(10, 18)
        gridIndex.append(i)
        gridValue.append(value)
        gridToll.append(int(value/3))

    return (gridIndex, gridValue, gridToll)

# Initial playerlist and boardlist
def initial_state() -> tuple:
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

def drop_lucky_box(state: tuple) -> list: 
    global grid
    tempgrid = grid
    
    boxes = random.randint(int(tempgrid/8), int(tempgrid/5)) # initialize the number of lucky boxes (randomly droped)
    
    res = state[1]

    indexList = board_grid_value(tempgrid)[0]
    boxSpots = random.sample(indexList, boxes)
    cellList = []
    for i in range(len(boxSpots)):
        cellList = list(res[boxSpots[i]][0])
        cellList[0] = 1
        newCellTuple = tuple(cellList)

        res[boxSpots[i]] = (newCellTuple, res[boxSpots[i]][1])

    return res

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
    return (orderlist, dicenumlist) 

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
 
    return (playerlist, boardlist)

# [grid position, can open lucky box, grid can be occupied] = [?, 1, 1]
def valid_actions(state: tuple) -> list:
    playerlist = state[0]
    boardlist = state[1]
    actions_check = []
    for i in range(len(playerlist)):
        checklist = [-1, 0, 0]
        pos = playerlist[i][2]
        bcell = boardlist[pos]
        checklist[0] = pos
        if bcell[0][0] == 1: # luckybox droped here
            checklist[1] = 1
        if bcell[1][0] == 0: # no one occupy here
            checklist[2] = 1
        actions_check.append(checklist)

    return actions_check

def winner_of(player: list) -> int:
    winner = 0
    max = 0
    for i in range(n):
        hp_gold = 12 * player[i][1] 
        plist = list(player[i])
        plist[0] = player[i][0] + hp_gold
        if plist[0] >= max:
            max = plist[0] 
            winner = i
        plist[1] = 0
        newpTuple = tuple(plist)
        player[i] = newpTuple 
    
    return winner

# v = player_nextround_order(1)
# s = ([(50, 5, 3), (50, 5, 2)], [((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), 
#     ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 0))])
# valid_actions(s)
# move_one_round(v, s)

# Return a string of 4 digits. 
# first 2 digits: represent the index of all boardcells. 
# 3rd digit: represent whether this grid has lucky box or not (0: no lucky box. 1: has lucky box)
# 4th digit: represent whether this grid is occupied or not (0: no one occupied. 1: someone occupied)

# The string has three indented lines of text.
# The numbers should be padded and evenly spaced.
# If the number of grid is even (eg. 28), the string representation should be like:
# 
#              0000 0100 0200 0300 0400 0500 0600 0700 0800 0900 1000 1100 1200
#         2700                                                                  1300
#              2600 2500 2400 2300 2200 2100 2000 1900 1800 1700 1600 1500 1400
# 
# If the number of grid is odd (eg. 27), the string representation should be like:
# 
#              0000 0100 0200 0300 0400 0500 0600 0700 0800 0900 1000 1100 1200
#                                                                               1300
#              2600 2500 2400 2300 2200 2100 2000 1900 1800 1700 1600 1500 1400
# 
# Excluding the leading comment symbols "# " above, all blank space should match exactly:
#   There are exactly 8 blank spaces before the left (padded) number.
#   There is exactly 1 blank space between each (padded) pit number.
#   The returned string should start and end with new-line characters ("\n")
def string_of_boardIndex(board: list) -> str:
   
    # the number of grids is even
    if(grid % 2 == 0):
        edgeline = int(grid/2) # the number of grids in line 1 (= line 3)

        line1 = [pad(i)+str(board[1][i][0][0])+str(board[1][i][1][0]) for i in range(0, edgeline-1, 1)]
        newline1 = " ".join(line1)
        newline1 = '\n             ' + newline1 
        
        line2insert = ' '
        for i in range (0, edgeline - 1):
            line2insert += '     '

        line2start = pad(grid-1)+str(board[1][grid-1][0][0])+str(board[1][grid-1][1][0])
        line2end = pad(edgeline-1)+str(board[1][edgeline-1][0][0])+str(board[1][edgeline-1][1][0])

        line3 = [pad(i)+str(board[1][i][0][0])+str(board[1][i][1][0]) for i in range(grid-2, edgeline-1, -1)]
        newline3 = " ".join(line3)
        newline3 = '\n             ' + newline3

        outstr = newline1 +'\n        '+ line2start + line2insert + line2end + newline3+'\n'

    # the number of grids is odd
    else:
        edgeline = int(grid/2 + 1) # the number of grids in line 1 (= line 3)

        line1 = [pad(i)+str(board[1][i][0][0])+str(board[1][i][1][0]) for i in range(0, edgeline-1, 1)]
        newline1 = " ".join(line1)
        newline1 = '\n             ' + newline1 
        
        line2insert = ' '
        for i in range (0, edgeline - 1):
            line2insert += '     '
        line2new = pad(edgeline-1)+str(board[1][edgeline-1][0][0])+str(board[1][edgeline-1][1][0])

        line3 = [pad(i)+str(board[1][i][0][0])+str(board[1][i][1][0]) for i in range(grid-1, edgeline-1, -1)]
        newline3 = " ".join(line3)
        newline3 = '\n             ' + newline3

        outstr = newline1 +'\n          '+ line2insert + line2new + newline3+'\n'
    print(outstr)
    return outstr
