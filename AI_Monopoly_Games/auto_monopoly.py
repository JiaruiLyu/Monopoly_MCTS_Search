import game_session_helper
import Game as Game

# This file is for automating whole game sessions for AI training

if __name__ == "__main__":
    
    print("Welcome to AUTO Monopoly!")

    # Step 1: Choose game size
    # Step 2: Pick players, for now only two players
    # SINGLE SOURCE OF TRUTH for every info of the game

    grid_size = 8
    
    print("AUTO Game is ready to start!, grid size = {}, player zero is a Baseline AI, player one is a MCTS AI".format(grid_size))

    total_experiments = 100
    MCTS_win_count = 0
    player_zero_score = 0
    player_one_score = 0
    total_node_count = 0

    # create a file using grid_size as the name
    filename1 = "../experiment_output/auto_monopoly_nodecount_{}_Baseline{}_v_MCTS{}.txt".format(grid_size, Game.BASE_LINE_AI_MODE, Game.MCT_AI_MODE)
    filename2 = "../experiment_output/auto_monopoly_score_{}_Baseline{}_v_MCTS{}.txt".format(grid_size, Game.BASE_LINE_AI_MODE, Game.MCT_AI_MODE)
    f_count = open(filename1, "w")
    f_score = open(filename2, "w")


    print("max round: {}".format(Game.MAX_ROUND))
    print("baseline ai mode: {}. (0 for random, 1 for greedy)".format(Game.BASE_LINE_AI_MODE))
    print("mcts ai mode: {}. (0 for random, 1 for uct improved)".format(Game.MCT_AI_MODE))

    # Step 3: Start the game
    for i in range (total_experiments):
        print (" ----- Experiment {} / {} -----".format(i, total_experiments))
        game: Game = game_session_helper.game_auto_setup(grid_size, 1, 2)
        while (not game.is_game_over(verbose=False)):
            game.play_one_turn(verbose=False) # will call the user or ai to play a turn
        if (game.announce_winner(verbose=False) == 1):
            MCTS_win_count += 1
            print("MCTS AI wins! by {} to {}".format(game.player_list[1].money, game.player_list[0].money))
        else:
            print("MCTS AI loses! by {} to {}".format(game.player_list[1].money, game.player_list[0].money))
        # print("MCTS processed {} nodes in this game".format(game.mct_node_count))
        f_count.write("{}\n".format(game.mct_node_count))
        f_score.write("{}\n".format(game.player_list[1].money - game.player_list[0].money))

        total_node_count += game.mct_node_count
        player_zero_score += game.player_list[0].money
        player_one_score += game.player_list[1].money

        # game.print_info()
        
        print("Experiment {} finished.".format(i))

    f_count.close()
    f_score.close()

    # evaluation: winrate, average score...
    print("Evaluation: ")
    print("MCTS win rate: {}".format(MCTS_win_count / total_experiments))
    print("MCTS average score: {} / baseline average score: {} = {}".format(player_one_score / total_experiments, player_zero_score / total_experiments, player_one_score / player_zero_score))
    print("MCTS average node count: {}".format(total_node_count / total_experiments))

    