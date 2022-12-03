# Monte Carlo Tree Search

# Step 1: Do random rollouts to get a good estimate of the value of each action, make sure to add dice layers

# Step 2: Use UTC to select the best action for the next rollout

# Step 3: Repeat for a couple of time (When to stop, good question...)


import numpy as np

from Player import Player
from BoardCell import BoardCell
import random
import utils
import copy

class StateNode:
    def __init__(self, game):
        self.visit_count = 0
        self.utility = 0
        self.children = [] # a list of child StateNode objects
        # <= 12 actions -> <= 12 children
        self.action = []

        self.parent = None # parent ChanceNode object

        self.game_state = game # Game type

    def populate_children(self):
        # 1. role dice -> 2. take action
        sub_state_list = self.game_state.get_all_sub_games()
        for sub_state in sub_state_list:
            self.children.append(StateNode(sub_state))
    def add_child(self, child):
        self.children.append(child)

    def set_parent(self, parent):
        self.parent = parent
    def get_visit_count(self) -> int:
        return self.visit_count
    def set_visit_count(self, visit_count):
        self.visit_count = visit_count
    def increment_visit_count(self):
        self.visit_count += 1

    def get_utility(self):
        return self.utility
    def set_utility(self, utility):
        self.utility = utility
    def set_game(self, game):
        self.game = game

    def get_random_child(self):
        rnd_index = random.randint(0, len(self.children)-1)
        return self.children[rnd_index]

def rnd_roll_out_helper(curr_node, ancester, node_count):

    # base case
    if (curr_node.game_state.is_game_over(verbose=False)):
        score = curr_node.game_state.get_score(ancester)
        curr_node.increment_visit_count()
        curr_node.set_utility(score)
        return node_count+1

    # pick a random child
    curr_node.populate_children()
    next_node = curr_node.get_random_child()

    rnd_roll_out_helper(next_node, ancester, node_count)

    new_total = curr_node.get_utility() * curr_node.get_visit_count() + next_node.get_utility()
    curr_node.increment_visit_count()
    new_util = new_total/curr_node.get_visit_count()
    curr_node.set_utility(new_util)

    return node_count+1

def UCT_roll_out_helper(curr_node, ancester, depth):

    # base case
    if (curr_node.game_state.is_game_over(verbose=False)):
        score = curr_node.game_state.get_score(ancester)
        curr_node.increment_visit_count()
        curr_node.set_utility(score)
        return

    # pick a random child
    curr_node.populate_children()
    # next_node = curr_node.get_random_child() # pick child based on UCT

    UCT_roll_out_helper(next_node, ancester, depth)

    new_total = curr_node.get_utility() * curr_node.get_visit_count() + next_node.get_utility()
    curr_node.increment_visit_count()
    new_util = new_total/curr_node.get_visit_count()
    curr_node.set_utility(new_util)

    pass

def roll_out(game, mct_ai_mode = 0, verbose: bool = True) -> tuple:
    
    curr_game = copy.deepcopy(game) # run roll_out on this copy so it does not mess up the actual game data.
    
    root = StateNode(curr_game)

    # at this point, the AI has two possible moves, purchase land or do nothing, run roll out on both
    # add the two children to the root node
    # and run roll_out_helper on each child
    root.add_child(StateNode(curr_game))

    curr_game_b = copy.deepcopy(game)
    curr_game_b.purchase_land()
    root.add_child(StateNode(curr_game_b))

    node_count = 0
    
    if (mct_ai_mode == 0):
        for i in range(20):
            node_count += rnd_roll_out_helper(root.children[0], curr_game.player_in_turn, 0)
            node_count += rnd_roll_out_helper(root.children[1], curr_game.player_in_turn, 0)
    elif (mct_ai_mode == 1):
        # use UCT to select the best child
        for i in range(20):
            UCT_roll_out_helper(root.children[0], curr_game.player_in_turn, 0)
            UCT_roll_out_helper(root.children[1], curr_game.player_in_turn, 0)

    # choose the child that has the maximum utility
    
    a = root.children[0].get_utility()
    b = root.children[1].get_utility()

    if verbose:
        print("roll_out OVER")

    if (a > b) :
        return (0, node_count)
    else:
        return (1, node_count)