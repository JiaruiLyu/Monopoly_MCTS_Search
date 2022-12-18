import random
import numpy as np
import game_session_helper


# data file format:
# 1. 1 x 16 grid
# 2. 2 players
# 3. AI always player 1 (second)
# 4. each row represent one data point (a random game state (10-20 turns))
# 5. each data point is a 1D array
# 6. each 1D array has: 16 * 7 + 2 + 1 + 1= 116 elements
# 7. the first 16 * 7 elements, each 16 length subarray represent:
#    player 0 location
#    player 1 location
#    player 0 ownership
#    player 1 ownership
#    land price
#    land rent
#    lucky box amount
# 8. the next 2 elements represent player 0 money and player 1 money, at that point
# 9. the next 1 element represent the turn count
# 10. the next 1 element represent the score of player 0 at the end of that game

def generate_data(filename: str, num_games: int = 2000):
    # create a data storing file
    testfile = open(filename, "w")
    bad_data_flag = False

    # play a random number of rounds
    for i in range(num_games):
        game = game_session_helper.game_auto_setup(16, 1, 1)
        for i in range (random.randint(0, 24)):
            game.play_one_turn(verbose=False)
            if (game.is_game_over(verbose=False)):
                bad_data_flag = True
                break
        
        if bad_data_flag:
            bad_data_flag = False
            continue
        game_data = game.port_data().flatten() # flatten the matrix into a 1D array
        game_data = np.append(game_data, game.turn_count) # append turn count
        game_data = np.append(game_data, game.player_list[0].money) # append the money of player 0
        game_data = np.append(game_data, game.player_list[1].money) # append the money of player 1

        # write the output to the 1D array
        while not game.is_game_over(verbose=False):
            game.play_one_turn(verbose=False)
        game_data = np.append(game_data, game.get_score(1)) # append the score

        # write the data to the file
        for i in range(len(game_data)):
            testfile.write("{},".format(game_data[i]))
        testfile.write("\n")

    pass

if __name__ == "__main__":
    generate_data("data_zzhang96/train_data.csv")
    generate_data("data_zzhang96/test_data.csv", 500)
