from bots.defensive_and_optimal_expansion import DefensiveAndOptimalExpansionBot
from game.team import Team
from map_generation.even_distribution_map_generator import EvenDistributionMapGenerator
from map_generation.spoke_map_generator import SpokeMapGenerator
from bots.random_bot import RandomBot
from bots.full_aggression_bot import FullAggressionBot
from bots.split_closest_friend_and_other import SplitClosestFriendAndOther
from bots.optimal_expansion_bot import OptimalExpansionBot
from game.player import Player
from game.game import Game
import json
import gzip

GAME_NAME = "ExampleGame"

bot_split = SplitClosestFriendAndOther()
bot_random_1 = RandomBot()
bot_random_2 = RandomBot()
bot_aggressive = FullAggressionBot()
bot_optimal = OptimalExpansionBot()
bot_optim_def_1 = DefensiveAndOptimalExpansionBot()
bot_optim_def_2 = DefensiveAndOptimalExpansionBot()

team_1 = Team("team_1", "red")

player_split = Player("Split", "red", bot_split.create_orders, team=team_1)
player_random_1 = Player("Random 1", "blue", bot_random_1.create_orders)
player_random_2 = Player("Random 2", "orange", bot_random_2.create_orders)
player_aggressive = Player("Aggressive", "green", bot_aggressive.create_orders)
player_optimal = Player("OptimalExpansion", "yellow", bot_optimal.create_orders, team=team_1)
player_optim_def_1 = Player("optim_def_1", "pink", bot_optim_def_1.create_orders)
player_optim_def_2 = Player("optim_def_2", "purple", bot_optim_def_2.create_orders)

player_list = [
  # player_aggressive,
  # player_random_1,
  # player_random_2,
  player_split,
  player_optimal,
  player_optim_def_1,
  # player_optim_def_2
  ]

starting_map = EvenDistributionMapGenerator(30, 10, player_list).create_map()

game = Game(player_list, starting_map, max_turn_limit=1000)
game.run()

print(f"THE WINNER IS: {[winner.name for winner in game.winners]}")

with gzip.open(f"games/{GAME_NAME.replace(" ", "")}.json.gz", "wt", encoding="ascii") as zip_file:
    json.dump(game.to_json(), zip_file, separators=(",", ":"))

print("end")
