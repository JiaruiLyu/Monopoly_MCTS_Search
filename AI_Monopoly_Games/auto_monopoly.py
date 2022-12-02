import game_session_helper
from Game import *

# This file is for automating whole game sessions for AI training

if __name__ == "__main__":
	
	print("Welcome to AUTO Monopoly!")

	# Step 1: Choose game size
	# Step 2: Pick players, for now only two players
	# SINGLE SOURCE OF TRUTH for every info of the game
	game: Game = game_session_helper.game_setup()

	print("Game is ready to start!")
	game.print_info()

	# Step 3: Start the game
	while (not game.is_game_over()):
		game.play_one_turn() # will call the user or ai to play a turn
		game.print_info()

	game.announce_winner()