from map_generation.even_distribution_map_generator import EvenDistributionMapGenerator
from bots.random_bot import RandomBot
from bots.full_aggression_bot import FullAggressionBot
from bots.split_closest_friend_and_other import SplitClosestFriendAndOther
from game.player import Player
from game.game import Game
from game_draw.draw_game import draw_game

bot_1 = SplitClosestFriendAndOther()
bot_2 = RandomBot()
bot_3 = FullAggressionBot()

player_1 = Player("Split", "red", bot_1.create_orders)
player_2 = Player("Random", "blue", bot_2.create_orders)
player_3 = Player("Aggressive", "green", bot_3.create_orders)

player_list = [player_1, player_2, player_3]

map = EvenDistributionMapGenerator(10, 5, player_list).create_map()

game = Game(player_list, map.planets, max_turn_limit=50)
game.run()

print(f"THE WINNER IS: {game.winner.name}")

# from pprint import pprint
# for planet in game.current_state.planets:
#     pprint(vars(planet))

draw_game(game.history)

print("end")