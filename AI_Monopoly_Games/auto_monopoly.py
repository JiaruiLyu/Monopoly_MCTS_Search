import game_session_helper
from Game import *

# This file is for automating whole game sessions for AI training

if __name__ == "__main__":
    
    print("Welcome to AUTO Monopoly!")

    # Step 1: Choose game size
    # Step 2: Pick players, for now only two players
    # SINGLE SOURCE OF TRUTH for every info of the game
    
    print("AUTO Game is ready to start!")

    total_experiments = 20
    MCTS_win_count = 0

    player_zero_score = 0
    player_one_score = 0

    # Step 3: Start the game
    for i in range (total_experiments):
        print (" ----- Experiment {} -----".format(i))
        game: Game = game_session_helper.game_auto_setup(20, 1, 2)
        while (not game.is_game_over(verbose=False)):
            game.play_one_turn(verbose=False) # will call the user or ai to play a turn
        if (game.announce_winner(verbose=False) == 1):
            MCTS_win_count += 1
            print("MCTS AI wins! by {} to {}".format(game.player_list[1].money, game.player_list[0].money))
        else:
            print("MCTS AI loses! by {} to {}".format(game.player_list[1].money, game.player_list[0].money))

        player_zero_score += game.player_list[0].money
        player_one_score += game.player_list[1].money
        
        print("Experiment {} finished.".format(i))

    # evaluation: winrate, average score...
    print("Evaluation: ")
    print("Baseline AI average score: {}".format(game.player_list[0].money / total_experiments))
    print("MCTS win rate: {}".format(MCTS_win_count / total_experiments))
    print("Baseline AI average score: {}".format(player_zero_score / total_experiments))
    print("MCTS average score: {}".format(player_one_score / total_experiments))


    