from monopoly_helpers import *

if __name__ == "__main__":
	game_state = initial_state()  
	round = 0

	while (game_over(game_state) == False):
		player_nextround_order(round)