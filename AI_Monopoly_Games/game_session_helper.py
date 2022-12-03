from Game import *

def game_setup():

	game: Game
    # Step 1: Choose game size
	while (True):
		prompt = "Please choose the size of the game board: A: 16, B: 18, C: 20, D: 22, E: 24: \n"
		game_size_choice = input(prompt)
		choice_int = min(abs(ord(game_size_choice) - ord('A')), abs(ord(game_size_choice) - ord('a')))
		if (choice_int < 0 or choice_int > 4):
			print("Invalid input, please try again.")
		else:
			game_size = 16 + 2 * choice_int
			print("You have chosen a game board of size {}.".format(game_size))
			game = Game(grid_size=game_size)
			break
	
	# Step 2: Pick players, for now only two players
	while (True):
		prompt = "Please choose player type for PLAYER ZERO: A: Human, B: Baseline AI, C: MCTS AI \n"
		player_zero_choice = input(prompt)
		choice_int = min(abs(ord(player_zero_choice) - ord('A')), abs(ord(player_zero_choice) - ord('a')))
		if (choice_int < 0 or choice_int > 2):
			print("Invalid input, please try again.")
		else:
			player_zero_type = choice_int
			game.set_player_type(0, player_zero_type)
			break
	
	while (True):
		prompt = "Please choose player type for PLAYER ONE: A: Human, B: Baseline AI, C: MCTS AI \n"
		player_one_choice = input(prompt)
		choice_int = min(abs(ord(player_one_choice) - ord('A')), abs(ord(player_one_choice) - ord('a')))
		if (choice_int < 0 or choice_int > 2):
			print("Invalid input, please try again.")
		else:
			player_one_type = choice_int
			game.set_player_type(1, player_one_type)
			break
	return game
pass

def game_auto_setup(grid_size: int = 20, player_zero_type: int = 1, player_one_type: int = 2):
	# print("This is an auto game experiment, default: grid size = 20, player zero is a Baseline AI, player one is a MCTS AI")

	game = Game(grid_size)
	
	# Step 2: Pick players, for now only two players
	game.set_player_type(0, player_zero_type) # Baseline AI
	game.set_player_type(1, player_one_type) # MCTS AI
	return game
pass