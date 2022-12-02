from Player import Player
from BoardCell import BoardCell
import random

class Game:
    # Initialize all the game stats, SINGLE SOURCE OF TRUTH for everyinfo of the game
    def __init__(self, grid_size: int = 20):
        self.round_count = 0
        self.player_count = 2
        self.grid_size = grid_size
        self.user_turn = 0  # 0 means player 0's turn, 1 means player 1's turn, etc.

        self.player_list = [] # list of Player objects
        self.board_list = [] # list of BoardCell objects

        ### Initialize players ###
        for i in range(self.player_count):
            new_player = Player(i)
            self.player_list.append(new_player)

        ### Initialize Board ###
        for i in range(self.grid_size):
            cell = BoardCell(i)
            self.board_list.append(cell) 

        # Drop players
        for i in range(self.player_count):
            self.board_list[0].add_player(i)

        # Drop lucky boxes
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

    # Print all cells in a circular order, each cell is 10 characters wide
    def board_to_string(self):
        result = ""
        cell_string_list = []
        for cell in self.board_list:
            cell_string_list.append(cell.to_string())

        print_width = self.grid_size//2//2
        print_height = self.grid_size//2 - print_width
        space_filler = " " * 25

        #  e.g. 14
        #  00 01 02
        #  13    03
        #  12    04
        #  11    05
        #  10    06
        #  09 08 07

        result += "\n " + " ".join(cell_string_list[0:print_width]) + "\n"
        curr_index = print_width
        result += "\n"
        for i in range(print_height):
            result += " "
            result += cell_string_list[print_width*2+print_height*3-curr_index-1] + " " + space_filler*(print_width-2) + cell_string_list[curr_index] + "\n"
            curr_index += 1
            result += "\n"
        result += " " + " ".join(cell_string_list[curr_index:curr_index+print_width][::-1]) + "\n"
        
        return result

    def players_to_string(self):
        result = ""
        for player in self.player_list:
            result += player.to_string() + "\n"
        return result

    def print_info(self):
        print("\n ==== Map Representation: ===== \n [ID O: Owner, P: Land Price; R: Land Rent; L: Lucky Box Amount, | Players on the cell ] \n")
        print(" ========== Round: " + str(self.round_count) + " ==========")
        print(self.players_to_string())
        print(self.board_to_string())

    def set_player_type(self, index: int, type: int):
        self.player_list[index].set_type(type)

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
