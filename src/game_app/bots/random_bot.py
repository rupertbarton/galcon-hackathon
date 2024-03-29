from bots.abstract_bot import AbstractBot
from game.galaxy import Galaxy
from game.player import Player

import random


class RandomBot(AbstractBot):

    def create_orders(self, current_player: Player, current_state: Galaxy):
        super().create_orders(current_player, current_state)

        orders = []
        for planet in self.own_planets:
            if random.random() > 0.5:
                new_order = {
                    "source": planet,
                    "destination": random.choice(self.current_state.planets),
                    "troop_count": planet.troop_count * random.random()
                }
                orders.append(new_order)
        return orders