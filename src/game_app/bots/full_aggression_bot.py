from bots.abstract_bot import AbstractBot
from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from bots.utils import find_nearest_planet


class FullAggressionBot(AbstractBot):

    def __init__(self):
        super().__init__()
        self.current_target: Planet = None

    def create_orders(self, current_player: Player, current_state: Galaxy):
        super().create_orders(current_player, current_state)

        orders = []

        if self.current_target is None or (
            self.current_target and self.is_friendly_planet(self.current_target)
        ):
            self.current_target = find_nearest_planet(
                (
                    self.current_target.position
                    if self.current_target
                    else self.own_planets[0].position
                ),
                self.enemy_planets,
            )

        for planet in self.own_planets:
            new_order = {
                "source": planet,
                "destination": self.current_target,
                "troop_count": planet.troop_count,
            }
            orders.append(new_order)
        return orders
