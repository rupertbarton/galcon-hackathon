from map_generation.even_distribution_map_generator import EvenDistributionMapGenerator
from map_generation.spoke_map_generator import SpokeMapGenerator
from bots.random_bot import RandomBot
from bots.full_aggression_bot import FullAggressionBot
from bots.split_closest_friend_and_other import SplitClosestFriendAndOther
from bots.optimal_expansion import OptimalExpansion
from game.player import Player
from game.game import Game
from game_draw.draw_game import draw_game
import json
import gzip

bot_1 = SplitClosestFriendAndOther()
bot_2 = RandomBot()
bot_3 = FullAggressionBot()
bot_4 = OptimalExpansion()

player_1 = Player("Split", "red", bot_1.create_orders)
player_2 = Player("Random", "blue", bot_2.create_orders)
player_3 = Player("Aggressive", "green", bot_3.create_orders)
player_4 = Player("OptimalExpansion", "yellow", bot_4.create_orders)

player_list = [
    player_3, 
player_2, 
player_1, 
player_4]

starting_map = SpokeMapGenerator(20, 10, player_list).create_map()

game = Game(player_list, starting_map, max_turn_limit=1000)
game.run()

print(f"THE WINNER IS: {[winner.name for winner in game.winners]}")

# draw_game(game.history)

with gzip.open("sample.json.gz", "wt", encoding="ascii") as zip_file:
    json.dump(game.to_json(), zip_file, separators=(",", ":"))

print("end")
