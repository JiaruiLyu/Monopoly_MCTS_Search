from Game import *

if __name__ == "__main__":
	# Step 1: Choose game size
	print("Welcome to Monopoly!")

	game: Game
	game_size = None 
	player_zero_type = None # 0 for human, 1 for Baseline AI, 2 for MCTS AI
	player_one_type = None # 0 for human, 1 for Baseline AI, 2 for MCTS AI

	while (True):
		prompt = "Please choose the size of the game board: A: 16, B: 18, C: 20, D: 22, E: 24: \n"
		game_size_choice = input(prompt)
		if (ord(game_size_choice) - ord('A') < 0 or ord(game_size_choice) - ord('A') > 4):
			print("Invalid input, please try again.")
		else:
			game_size = 20 + 2 * (ord(game_size_choice) - ord('A'))
			game = Game(grid_size=game_size)
			break
	
	# Step 2: Pick players, for now only two players
	while (True):
		prompt = "Please choose player type for PLAYER ZERO: A: Human, B: Baseline AI: \n"
		player_zero_choice = input(prompt)
		if (ord(player_zero_choice) - ord('A') < 0 or ord(player_zero_choice) - ord('A') > 1):
			print("Invalid input, please try again.")
		else:
			player_zero_type = ord(player_zero_choice) - ord('A')
			game.set_player_type(0, player_zero_type)
			break
	
	while (True):
		prompt = "Please choose player type for PLAYER ONE: A: Human, B: Baseline AI: \n"
		player_one_choice = input(prompt)
		if (ord(player_one_choice) - ord('A') < 0 or ord(player_one_choice) - ord('A') > 1):
			print("Invalid input, please try again.")
		else:
			player_one_type = ord(player_one_choice) - ord('A')
			game.set_player_type(1, player_one_type)
			break

	# Step 3: Start the game
	game.print_info()
	
