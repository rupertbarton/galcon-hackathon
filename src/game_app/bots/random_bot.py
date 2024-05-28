
import random

from src.game_app.bots.abstract_bot import AbstractBot
from src.game_app.game.galaxy import Galaxy
from src.game_app.game.player import Player


class RandomBot(AbstractBot):

    def create_orders(self, current_player: Player, current_state: Galaxy):
        super().create_orders(current_player, current_state)

        # random.seed(225436234543)

        orders = []
        for planet in self.own_planets:
            if random.random() > 0.5:
                new_order = {
                    "source": planet.id,
                    "destination": random.choice(self.current_state.planets).id,
                    "troop_count": planet.troop_count * random.random(),
                }
                orders.append(new_order)
        return orders
