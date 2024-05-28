import gzip
import json

from bots.defensive_and_optimal_expansion import DefensiveAndOptimalExpansionBot
from bots.full_aggression_bot import FullAggressionBot
from bots.optimal_expansion_bot import OptimalExpansionBot
from bots.random_bot import RandomBot
from bots.split_closest_friend_and_other import SplitClosestFriendAndOther
from game.game import Game
from game.player import Player
from map_generation.even_distribution_map_generator import EvenDistributionMapGenerator
from src.game_app.bots.dales_bot import DalesBot

bot_1 = SplitClosestFriendAndOther()
bot_2 = RandomBot()
bot_3 = FullAggressionBot()
bot_4 = OptimalExpansionBot()
bot_5 = DefensiveAndOptimalExpansionBot()
bot_6 = DalesBot()

player_1 = Player("Split", "red", bot_1.create_orders)
player_2 = Player("Random", "blue", bot_2.create_orders)
player_3 = Player("Aggressive", "green", bot_3.create_orders)
player_4 = Player("OptimalExpansion", "yellow", bot_4.create_orders)
player_5 = Player("DefensiveAnOptimalExpansionBot", "pink", bot_5.create_orders)
player_6 = Player("Dale", "purple", bot_6.create_orders)

player_list = [
  # player_1, # split
  # player_2, # random
  # player_3, # Aggressive
  # player_4, # Expansion
  player_5, # Defend and expand
  player_6
  ]

starting_map = EvenDistributionMapGenerator(30, 20, player_list).create_map()

game = Game(player_list, starting_map, max_turn_limit=1000)
game.run()

print(f"THE WINNER IS: {[winner.name for winner in game.winners]}")

# draw_game(game.history)

with gzip.open("sample.json.gz", "wt", encoding="ascii") as zip_file:
    json.dump(game.to_json(), zip_file, separators=(",", ":"))

print("end")
