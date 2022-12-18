import numpy as np
import torch as tr
import matplotlib.pyplot as plt
import mcts
import Game

import game_session_helper
import nn_jlyu17

# read from the data generated (check data_generation.py for more info) 

class LinNet(tr.nn.Module):
    def __init__(self, input_size=115, hidden_size=32, output_size=1):
        super().__init__()
        self.to_hidden_1 = tr.nn.Linear(input_size, hidden_size)
        self.to_output = tr.nn.Linear(hidden_size, output_size)
        tr.nn.init.xavier_uniform_(self.to_hidden_1.weight)

    def forward(self, x):
        h_1 = tr.relu(self.to_hidden_1(x.reshape(x.shape[0],-1)))
        y = self.to_output(h_1)

        return y

def train_model():
    tmp_data = np.genfromtxt('data_zzhang96/train_data.csv', delimiter=',')
    tmp_testing_data = np.genfromtxt('data_zzhang96/test_data.csv', delimiter=',')
    input_data = tmp_data[:, 0:115].reshape(-1, 115)
    output_data = tmp_data[:, 115].reshape(-1, 1)
    input_test_data = tmp_testing_data[:, 0:115].reshape(-1, 115)
    output_test_data = tmp_testing_data[:, 115].reshape(-1, 1)

    curves = [], []

    print(input_data.shape)
    print(output_data.shape)

    # train the neural network
    my_nn = LinNet()
    loss_fn = tr.nn.MSELoss()
    optimizer = tr.optim.SGD(my_nn.parameters(), lr=0.000001)

    # convert the data to tensor
    tr_input_data = tr.from_numpy(input_data).float()
    tr_output_data = tr.from_numpy(output_data).float()
    tr_test_input_data = tr.from_numpy(input_test_data).float()
    tr_test_output_data = tr.from_numpy(output_test_data).float()

    for i in range(500):
        # forward pass
        y_pred = my_nn(tr_input_data)
        loss = loss_fn(y_pred, tr_output_data)

        # backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # print the loss
        # print("epoch: {}, loss: {}".format(i, loss.item()))
        curves[0].append(loss.item())

        # test the model
        y_pred_test = my_nn(tr_test_input_data)
        loss_test = loss_fn(y_pred_test, tr_test_output_data)
        curves[1].append(loss_test.item())

    # plot the loss curve
    # plt.plot(curves[0], label='train')
    # plt.plot(curves[1], label='test')
    # plt.legend()
    # plt.show()

    return my_nn

def game_to_model_input(game):
    # convert the game to a model input

    game_data = game.port_data().flatten() # flatten the matrix into a 1D array
    game_data = np.append(game_data, game.turn_count) # append turn count
    game_data = np.append(game_data, game.player_list[0].money) # append the money of player 0
    game_data = np.append(game_data, game.player_list[1].money) # append the money of player 1

    model_input = tr.from_numpy(game_data).float()
    # reshape data
    model_input = model_input.reshape(1, -1)

    return model_input

def run_experiments(nn_model):
    grid_size = 16
    
    print("Experiment is ready to start!, grid size = {}, player zero is a Baseline AI, player one is a MCTS AI".format(grid_size))

    total_experiments = 100
    MCTS_win_count = 0
    player_zero_score = 0
    player_one_score = 0
    total_node_count = 0

    # create a file using grid_size as the name
    filename1 = "../experiment_output/zz_nn_nodecount_{}_Baseline{}_v_MCTS{}.txt".format(grid_size, Game.BASE_LINE_AI_MODE, Game.MCT_AI_MODE)
    filename2 = "../experiment_output/zz_nn_monopoly_score_{}_Baseline{}_v_MCTS{}.txt".format(grid_size, Game.BASE_LINE_AI_MODE, Game.MCT_AI_MODE)
    f_count = open(filename1, "w")
    f_score = open(filename2, "w")


    print("max round: {}".format(Game.MAX_ROUND))
    print("baseline ai mode: {}. (0 for random, 1 for greedy)".format(Game.BASE_LINE_AI_MODE))
    print("mcts ai: NN".format(Game.MCT_AI_MODE))

    # Step 3: Start the game
    for i in range (total_experiments):
        print (" ----- Experiment {} / {} -----".format(i, total_experiments))
        game: Game = game_session_helper.game_auto_setup(grid_size, 1, 3)
        game.mct_nn_model = nn_model

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


def run_experiments_jiarui(nn_model):
    grid_size = 16
    
    print("Experiment is ready to start!, grid size = {}, player zero is a Baseline AI, player one is a MCTS AI".format(grid_size))

    total_experiments = 100
    MCTS_win_count = 0
    player_zero_score = 0
    player_one_score = 0
    total_node_count = 0

    # create a file using grid_size as the name
    filename1 = "../experiment_output/jl_nn_nodecount_{}_Baseline{}_v_MCTS{}.txt".format(grid_size, Game.BASE_LINE_AI_MODE, Game.MCT_AI_MODE)
    filename2 = "../experiment_output/jl_nn_monopoly_score_{}_Baseline{}_v_MCTS{}.txt".format(grid_size, Game.BASE_LINE_AI_MODE, Game.MCT_AI_MODE)
    f_count = open(filename1, "w")
    f_score = open(filename2, "w")


    print("max round: {}".format(Game.MAX_ROUND))
    print("baseline ai mode: {}. (0 for random, 1 for greedy)".format(Game.BASE_LINE_AI_MODE))
    print("mcts ai: NN".format(Game.MCT_AI_MODE))

    # Step 3: Start the game
    for i in range (total_experiments):
        print (" ----- Experiment {} / {} -----".format(i, total_experiments))
        game: Game = game_session_helper.game_auto_setup(grid_size, 1, 3)
        game.mct_nn_model = nn_model

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



if __name__ == "__main__":
    # nn_model = train_model()

    # Next step: use the trained model to run MCTS, run experiments
    game = game_session_helper.game_auto_setup(grid_size=16, player_zero_type=1, player_one_type=3)

    # run_experiments(nn_model)


    # Help run Jiarui's model and experiment
    train_data = np.genfromtxt('train_data.csv', delimiter=',')
    test_data = np.genfromtxt('test_data.csv', delimiter=',')
    train_data = np.delete(train_data,118,axis=1)
    test_data = np.delete(test_data,118,axis=1)
    
    nn_model_2 = nn_jlyu17.configure_data(train_data, test_data)
    run_experiments_jiarui(nn_model_2)
