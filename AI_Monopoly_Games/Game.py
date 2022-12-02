from Player import Player
from BoardCell import BoardCell
import random

MAX_ROUND = 30

class Game:
    # Initialize all the game stats
    def __init__(self, grid_size: int = 20):
        self.round_count = 0
        self.player_count = 2
        self.grid_size = grid_size
        self.player_in_turn = 0  # 0 means player 0's turn, 1 means player 1's turn, etc.

        self.player_list = [] # list of Player objects
        self.board_list = [] # list of BoardCell objects
        self.player_locations = [] # list of player locations, in the same order as self.player_list

        self.game_over_flag = False # flag used to stop the game loop

        ### Initialize players ###
        for i in range(self.player_count):
            new_player = Player(i)
            self.player_list.append(new_player)

        ### Initialize Board ###
        for i in range(self.grid_size):
            cell = BoardCell(i)
            self.board_list.append(cell) 

        # Drop players on the cells
        for i in range(self.player_count):
            self.board_list[0].add_player(i)
            self.player_locations.append(0)

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

    # ===== Helper Functions =====
    # DONE
    # move a player from one cell to another 
    # by making changes to data sources accordingly
    def move_player(self, playerindex: int, dicenum: int):
        currentlocation = self.player_locations[playerindex]
        newlocation = (currentlocation + dicenum) % self.grid_size
        self.player_locations[playerindex] = newlocation
        self.board_list[currentlocation].remove_player(playerindex)
        self.board_list[newlocation].add_player(playerindex)

    # DONE
    # set player type, 0 for human, 1 for Baseline AI, 2 for MCTS AI
    def set_player_type(self, index: int, type: int):
        self.player_list[index].set_type(type)

    # ===== Printing Functions =====
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
    

    ### TODO ###
    # Roll the dice, move the player in turn
    # ask for user / AI input if needed
    # do money transaction if needed
    # update other new states if needed
    def play_one_turn(self):
        curr_player_index = self.player_in_turn
        curr_player = self.player_list[curr_player_index]
        
        # roll dice
        dice_num = random.randint(1, 6)
        print("Player " + str(self.player_in_turn) + " rolled " + str(dice_num) + " points.\n")

        # move player
        self.move_player(self.player_in_turn, dice_num)

        # process lucky box if needed

        # process rent if needed

        # process decision making
        if (curr_player.get_type() == 0):
            # human player
            pass
        elif (curr_player.get_type() == 1):
            # baseline AI
            pass
        elif (curr_player.get_type() == 2):
            # MCTS AI
            pass

        # update next player in turn
        self.player_in_turn = self.player_count - 1 - curr_player_index
        self.round_count += 1


    # ==== Player Related ====
    # TODO: return a list of valid actions for the current player
    def valid_actions(self, player_index: int) -> list:
        # can choose: purchase current cell, if available
        # must do: pick up lucky box, pay rent
        return []

    # ==== End of Game Related ====
    # Return True if the game is over, and False otherwise.
    # The game is over if any user has 0 hp and cant pay the tolls
    def is_game_over(self) -> bool:
        if (self.round_count >= MAX_ROUND):
            print("Game Over! The game has reached the maximum round count.")
            return True
        elif (self.game_over_flag):
            print("Game Over! Some players have been eliminated.")
            return True
        return False

    # check each player's stats, calculate total score by hp and gold
    # return the player with the highest score
    def winner_of(self) -> int:
        playerlist = self.player_list
        n = self.player_count
        winner = 0
        max_point = 0

        for i in range(n):
            hp_gold = 15 * playerlist[i][1] 
            player_score = playerlist[i][0] + hp_gold
            if player_score >= max_point:
                max_point = player_score 
                winner = i
        return winner
