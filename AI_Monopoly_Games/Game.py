from Player import Player
from BoardCell import BoardCell
import random

class Game:
    # Initialize all the game stats, SINGLE SOURCE OF TRUTH for everyinfo of the game
    def __init__(self):
        self.round_count = 0
        self.player_count = 2
        self.grid_size = 28
        self.user_turn = 0  # 0 means player 0's turn, 1 means player 1's turn, etc.

        self.player_list = [] # list of Player objects
        self.board_list = [] # list of BoardCell objects

        ### Initialize players ###
        for i in range(self.player_count):
            new_player = Player(i+1)
            self.player_list.append(new_player)

        ### Initialize Board ###
        for i in range(self.grid_size):
            cell = BoardCell(i)
            self.board_list.append(cell) 

        # Initialize the board with lucky boxes
        self.drop_lucky_box()

    # ==== Board Related ====

    # DONE
    # Pick a few random cells in self.board_list and set them as lucky boxes
    def drop_lucky_box(self):
        grid_size = self.grid_size
        box_count = random.randint(int(grid_size/8), int(grid_size/5))
        box_spots = random.sample(self.board_list, box_count)
        for cell in box_spots:
            cell.set_lucky_box(random.randint(2, 5))

    ### TODO ###
    def move_one_round(self, playerOrder: tuple, state: tuple) -> tuple:

        playerlist = self.player_list
        boardlist = self.board_list

        ind = playerOrder[0]
        addup = playerOrder[1]

        for i in range(n):   
            pList = list(playerlist[ind[i]])
            temp = pList[2] + addup[i]
            pList[2] = temp % self.grid_size
            newpTuple = tuple(pList)
            playerlist[ind[i]] = newpTuple 

    def player_nextround_order(self, roundnum: int) -> tuple:
    
        orderlist = [] #存储的是playerindex，按顺序的
        dicenumlist = []
        dicedict = {}
        sorteddict = []
        n = self.player_count

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



    # ==== Player Related ====
    def valid_actions(self, state: tuple) -> tuple:
        playerlist = self.player_list
        boardlist = self.board_list
        # open lucky box
        # grid occupy
        # pay tolls
        return (playerlist, boardlist)

    # ==== End of Game Related ====

    # Return True if the game is over, and False otherwise.
    # The game is over if any user has 0 hp and cant pay the tolls
    def game_over(self) -> bool:
        playerlist = self.player_list
        checkhp = 0
        for i in range(len(playerlist)):
            #只要有player是0 hp，不管有多少gold, 直接出局
            if (playerlist[i][1] == 0):
                checkhp = 1

        return bool(checkhp)

    # check each player's stats, calculate total score by hp and gold
    # return the player with the highest score
    def winner_of(self) -> int:
        playerlist = self.player_list
        n = self.player_count
        winner = 0
        max = 0

        for i in range(n):
            hp_gold = 15 * playerlist[i][1] 
            player_score = playerlist[i][0] + hp_gold
            if player_score >= max:
                max = player_score 
                winner = i
        return winner

    # Return a list that stores each grid's index
    def boardIndex(self) -> list:

        boardIndexlist = []
        for i in range(self.grid_size):
            boardIndexlist.append(i) # initilize boardIndex  

        return boardIndexlist  

# Return a string representation of num that is always two characters wide.
# Assume num is either one or two digits long.
# If num does not already have two digits, a leading "0" is inserted in front.
# For example, pad(12) is "12", and pad(1) is "01".
def pad(num: int) -> str:
    return str(num).zfill(2) 


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
