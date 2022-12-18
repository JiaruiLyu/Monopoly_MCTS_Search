from Player import Player
from BoardCell import BoardCell
import random
import numpy as np
import copy
import nn_zzhang96

import utils
import mcts

MAX_ROUND = 30
BASE_LINE_AI_MODE = 0 # 0 for random, 1 for greedy (pick best rent/price property)
MCT_AI_MODE = 0 # 0 for random, 1 for uct improved
NN_AI_MODE = 0 # 0 for zzhang, 1 for jlyu

class Game:

    # Initialize all the game stats
    def __init__(self, grid_size: int = 20):
        self.turn_count = 0
        self.player_count = 2
        self.grid_size = grid_size
        self.player_in_turn = 0  # 0 means player 0's turn, 1 means player 1's turn, etc.
        self.mct_node_count = 0
        self.mct_nn_model = nn_zzhang96.train_model()

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

    # Pick a few random cells in self.board_list and set them as lucky boxes
    def drop_lucky_box(self):
        grid_size = self.grid_size
        box_count = random.randint(int(grid_size/8), int(grid_size/5))
        box_spots = random.sample(self.board_list, box_count)
        for cell in box_spots:
            cell.set_lucky_box(random.randint(2, 5))

    # move a player from one cell to another 
    # by making changes to data sources accordingly
    def move_player_in_turn(self, dicenum: int, verbose: bool = True):
        playerindex = self.player_in_turn
        currentlocation = self.player_locations[playerindex]
        newlocation = (currentlocation + dicenum) % self.grid_size
        self.player_locations[playerindex] = newlocation
        self.board_list[currentlocation].remove_player(playerindex)
        self.board_list[newlocation].add_player(playerindex)
        if (verbose):
            print("Player {} moved from {} to {}".format(playerindex, currentlocation, newlocation))

    # set player type, 0 for human, 1 for Baseline AI, 2 for MCTS AI
    def set_player_type(self, index: int, type: int):
        self.player_list[index].set_type(type)

    def has_available_action(self) -> bool:
        curr_cell = self.board_list[self.player_locations[self.player_in_turn]]
        return not curr_cell.has_owner()

    def set_nn_model(self, model):
        self.mct_nn_model = model

    # ==== Data related ====
    # use matrix to represent the board for data processing
    def port_data(self) -> np.ndarray:
        # port all board data to a 3d matrix
        # matrix[0] = player 0 location
        # matrix[1] = player 1 location
        # matrix[2] = player 0 ownership
        # matrix[3] = player 1 ownership
        # matrix[4] = land price
        # matrix[5] = land rent
        # matrix[6] = lucky box amount
        matrix = np.zeros((7, self.grid_size))
        for i in range(self.grid_size):
            matrix[0][i] = self.player_locations[0] == i
            matrix[1][i] = self.player_locations[1] == i
            matrix[2][i] = self.board_list[i].get_owner() == 0
            matrix[3][i] = self.board_list[i].get_owner() == 1
            matrix[4][i] = self.board_list[i].get_price()
            matrix[5][i] = self.board_list[i].get_rent()
            matrix[6][i] = self.board_list[i].get_lucky_box_amount()

        return matrix 

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
            result += player.to_string() + " location: {}".format(self.player_locations[player.get_id()]) + "\n"
        return result

    def print_info(self):
        print("========== After Move Game Stat ==========")
        print("  ---------- Plyaers ----------")
        print(self.players_to_string())
        if (self.mct_node_count > 0):
            print(" total MCTS procssed node count: {}".format(self.mct_node_count))
        print("  ---------- Board ------------ (clockwise) \n [ID @: Owner, P: Land Price; R: Land Rent; L: Lucky Box Amount, | Players on the cell ]")
        print(self.board_to_string())
    

    # ==== Game Loop Related ====
    ### TODO ###
    # Roll the dice, move the player in turn
    # ask for user / AI input if needed
    # do money transaction if needed
    # update other new states if needed
    def play_one_turn(self , verbose: bool = True):
        curr_player_index = self.player_in_turn
        curr_player = self.player_list[curr_player_index]

        self.turn_count += 1
        if (verbose):
            print("========== Turn: " + str(self.turn_count) + " ==========")
        
        # roll dice
        dice_num = utils.roll_dice()
        if (verbose):
            print("Player " + str(curr_player_index) + " rolled " + str(dice_num) + " points.")

        # move player
        self.move_player_in_turn(dice_num, verbose)
        curr_player_location = self.player_locations[curr_player_index] # index after moving

        # process lucky box if needed, player gains money
        curr_cell = self.board_list[curr_player_location]
        if curr_cell.has_lucky_box():
            curr_player.add_money(curr_cell.get_lucky_box_amount())
            if verbose:
                print("Player " + str(curr_player_index) + " got lucky! " + str(curr_cell.get_lucky_box_amount()) + " cash added to his account.\n")

        # process rent if needed, player lose money, owner gains money
        if curr_cell.has_owner() and curr_cell.get_owner() != curr_player_index:
            curr_player.remove_money(curr_cell.get_rent())
            self.player_list[curr_cell.get_owner()].add_money(curr_cell.get_rent())
            if verbose:
                print("Player " + str(curr_player_index) + " paid rent to Player " + str(curr_cell.get_owner()) + ". " + str(curr_cell.get_rent()) + " cash removed from his account.\n")

        # process land purchase decision making
        if (not curr_cell.has_owner()):
            if (curr_player.get_type() == 0):
                # human player
                # ask for user input, purchase land or not, if available
                prompt = "Player " + str(curr_player_index) + " valid action: \n do you want to purchase this land? (y/n) "
                if (input(prompt) == "y"):
                    curr_cell.set_owner(curr_player_index)
                    curr_player.remove_money(curr_cell.get_price())
                    input(" Player " + str(curr_player_index) + " purchased this land for " + str(curr_cell.get_price()) + ". Enter to next turn.\n")
                    
                pass
            elif (curr_player.get_type() == 1):
                # baseline AI
                if verbose:
                    input("Player " + str(curr_player_index) + " is a baseline AI, press ENTER to proceed.")
                if ((BASE_LINE_AI_MODE == 0 and utils.flip_coin() == 1) or (BASE_LINE_AI_MODE == 1 and (curr_cell.get_price()/curr_cell.get_rent() < 2.5) and curr_player.get_money() >= curr_cell.get_price())):
                    curr_cell.set_owner(curr_player_index)
                    curr_player.remove_money(curr_cell.get_price())
                    if verbose:
                        input(" Player " + str(curr_player_index) + " purchased this land for " + str(curr_cell.get_price()) + ". Enter to next turn.\n")
                else:
                    if verbose:
                        input(" Player " + str(curr_player_index) + " decided not to purchase this land. Enter to next turn.\n")
                pass
            elif (curr_player.get_type() == 2):
                # MCTS AI
                if verbose:
                    input("Player " + str(curr_player_index) + " is a MCTS AI, press ENTER to proceed.")
                decision, node_count = mcts.roll_out(self, MCT_AI_MODE, verbose=verbose)
                self.mct_node_count += node_count
                if decision:
                    curr_cell.set_owner(curr_player_index)
                    curr_player.remove_money(curr_cell.get_price())
                    if verbose:
                        print(" Processed node count in this turn: " + str(node_count))
                        input(" Player " + str(curr_player_index) + " purchased this land for " + str(curr_cell.get_price()) + ". Enter to next turn.\n")
                else:
                    if verbose:
                        print(" Processed node count in this turn: " + str(node_count))
                        input(" Player " + str(curr_player_index) + " decided not to purchase this land. Enter to next turn.\n")
                pass

            elif (curr_player.get_type() == 3):
                # NN AI
                if verbose:
                    input("Player " + str(curr_player_index) + " is a NN AI, press ENTER to proceed.")
                if (NN_AI_MODE == 0):
                    decision, node_count = mcts.roll_out_NN_zz(self, self.mct_nn_model, verbose=verbose)
                else:
                    decision, node_count = mcts.roll_out_NN_jl(self, self.mct_nn_model, verbose=verbose)
                self.mct_node_count += node_count
                if decision:
                    curr_cell.set_owner(curr_player_index)
                    curr_player.remove_money(curr_cell.get_price())
                    if verbose:
                        print(" Processed node count in this turn: " + str(node_count))
                        input(" Player " + str(curr_player_index) + " purchased this land for " + str(curr_cell.get_price()) + ". Enter to next turn.\n")
                else:
                    if verbose:
                        print(" Processed node count in this turn: " + str(node_count))
                        input(" Player " + str(curr_player_index) + " decided not to purchase this land. Enter to next turn.\n")

                pass
        else:
            if verbose:
                input(" Player " + str(curr_player_index) + " is on a land owned by Player " + str(curr_cell.get_owner()) + ". \n There is no valid actions. Enter to next turn. \n")
        
        if (curr_player.get_money() < 0):
            self.game_over_flag = True
        
        # update next player in turn
        self.player_in_turn = self.player_count - 1 - curr_player_index

    # ==== End of Game Related ====
    # Return True if the game is over, and False otherwise.
    # The game is over if any user has 0 hp and cant pay the tolls
    def is_game_over(self, verbose: bool = True) -> bool:
        if (self.turn_count >= MAX_ROUND):
            if verbose:
                print("Game Over! The game has reached the maximum round count.")
            return True
        elif (self.game_over_flag):
            if verbose:
                print("Game Over! One player has been eliminated.")
        
        return self.game_over_flag

    # check each player's stats, calculate total score by hp and gold
    # return the player with the highest score
    def announce_winner(self, verbose: bool = True) -> int:
        winner = 0
        winner_score = 0
        for i in range(self.player_count):
            curr_score = self.player_list[i].get_score()
            if (curr_score > winner_score):
                winner = i
                winner_score = curr_score
        if verbose:
            print("Player " + str(winner) + " is the winner!")
        return winner

    def get_score(self, player_index) -> float:
        # assume two player only
        a = self.player_list[player_index].get_money()
        b = self.player_list[1-player_index].get_money()
        if (b <= 0):
            return a - b
        else:
            return a - b

    # ======= helpfer functions for state tree ======
    def get_all_sub_games(self) -> list:
        sub_game_list = []

        for i in range(6):
            dicenum = i+1
            sub_game = copy.deepcopy(self)
            sub_game.turn_count += 1
            sub_game.move_player_in_turn(dicenum, False)
            if (sub_game.has_available_action()):
                # choose between purchase land or not
                sub_game_b = copy.deepcopy(sub_game) # do nothing
                sub_game.purchase_land() # do something

                sub_game_list.append(sub_game_b)
                sub_game_list.append(sub_game)
            else:
                # pay rent, thats it
                sub_game.pay_rent()
                sub_game_list.append(sub_game)

        return sub_game_list

    def purchase_land(self):
        curr_cell = self.board_list[self.player_locations[self.player_in_turn]]
        curr_player = self.player_list[self.player_in_turn]
        
        curr_cell.set_owner(self.player_in_turn)
        curr_player.remove_money(curr_cell.get_price())

    def pay_rent(self):
        curr_cell = self.board_list[self.player_locations[self.player_in_turn]]
        curr_player = self.player_list[self.player_in_turn]

        curr_player.remove_money(curr_cell.get_rent())
        self.player_list[curr_cell.get_owner()].add_money(curr_cell.get_rent())