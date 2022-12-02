# Monte Carlo Tree Search

# Step 1: Do random rollouts to get a good estimate of the value of each action, make sure to add dice layers

# Step 2: Use UTC to select the best action for the next rollout

# Step 3: Repeat for a couple of time (When to stop, good question...)


import numpy as np

from Player import Player
from BoardCell import BoardCell
import utils
import copy

# TODO:
def roll_out_helper(curr_game, player_index):
    # base case
    if (curr_game.is_game_over()):
        return curr_game.get_winner()

    pass

def roll_out(game, player_index):
    
    curr_game = copy.deepcopy(game) # run roll_out on this copy so it does not mess up the actual game data.



    pass