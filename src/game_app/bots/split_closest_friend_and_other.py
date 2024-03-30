from bots.abstract_bot import AbstractBot
from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from bots.utils import find_nearest_planet



class SplitClosestFriendAndOther(AbstractBot):

    def __init__(self):
        super().__init__()

    def create_orders(self, current_player: Player, current_state: Galaxy):
        super().create_orders(current_player, current_state)

        orders = []

        for planet in self.own_planets:
            if len(self.friendly_planets) > 1:
                new_friend_order = {
                    "source": planet,
                    "destination": find_nearest_planet(planet.position, [p for p in  self.friendly_planets if not p.id == planet.id]),
                    "troop_count": planet.troop_count/2
                }
                orders.append(new_friend_order)
            
            if self.neutral_planets + self.enemy_planets:
                new_non_friend_order = {
                    "source": planet,
                    "destination": find_nearest_planet(planet.position, self.neutral_planets + self.enemy_planets),
                    "troop_count": planet.troop_count/2
                }
                orders.append(new_non_friend_order)
        return orders