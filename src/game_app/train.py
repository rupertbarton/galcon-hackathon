# BATCH_SIZE is the number of transitions sampled from the replay buffer
# GAMMA is the discount factor as mentioned in the previous section
# EPS_START is the starting value of epsilon
# EPS_END is the final value of epsilon
# EPS_DECAY controls the rate of exponential decay of epsilon, higher means a slower decay
# TAU is the update rate of the target network
# LR is the learning rate of the ``AdamW`` optimizer
import copy
import gzip
import json
from bots.dqn_ai.dqn_bot import DQNBot

from bots.random_bot import RandomBot
from game.game import Game
from game.player import Player
from map_generation.even_distribution_map_generator import EvenDistributionMapGenerator

import cProfile
import gc


random_bot = RandomBot()
random_player = Player("Random", "blue", random_bot.create_orders)

player_to_replace = Player("REPLACE_ME", "white", lambda: None)

player_list = [random_player, player_to_replace]

map_to_train = EvenDistributionMapGenerator(30, 10, player_list).create_map()

training_bot = DQNBot(map_to_train)
training_player = Player("DQN", "green", training_bot.handle_iteration)
training_bot_1 = DQNBot(map_to_train)
training_player_1 = Player("DQN", "pink", training_bot_1.handle_iteration)

for planet in map_to_train.planets:
    if planet.owner and planet.owner.id == player_to_replace.id:
        planet.owner = training_player
    if planet.owner and planet.owner.id == random_player.id:
        planet.owner = training_player_1
        
print("starting")

wins = 0
losses = 0

for i in range(100):
    game = Game([training_player_1, training_player], map_to_train.deep_copy(), max_turn_limit=10000)
    winners = game.run()
    # cProfile.run("game.run()")
    file_name = f"sample{i}.json.gz"
    
    did_bot_win = list(winners)[0].id == training_player.id
    print("Did bot win?", did_bot_win)
    if did_bot_win:
        wins += 1
    else:
        losses += 1
    print("Wins:", wins)
    print("Losses:", losses)
    
    with gzip.open(file_name, "wt", encoding="ascii") as zip_file:
        json.dump(game.to_json(), zip_file, separators=(",", ":"))
    print(f"Game saved to {file_name}")
    
    # training_bot.handle_iteration(training_player, current_state=game.current_state, game_win = did_bot_win)
    # training_bot_1.handle_iteration(training_player_1, current_state=game.current_state, game_win = not did_bot_win)
    print(i)
    del game
    
    gc.collect()
    print("Garbage collector activated")
    
    training_bot.save("0")
    training_bot_1.save("1")
    print("AI model saved")
    
