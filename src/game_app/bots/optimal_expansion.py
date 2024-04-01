from bots.abstract_bot import AbstractBot
from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from game.utils import get_distance
from bots.utils import time_to_travel
from game.fleet import Fleet


class OptimalExpansion(AbstractBot):

    def __init__(self):
        super().__init__()

    def create_orders(self, current_player: Player, current_state: Galaxy):

        current_state_dict = {**current_state.__dict__}
        super().create_orders(current_player, current_state)
        planet_fleet_statuses = {}
        for planet in self.neutral_planets + self.enemy_planets:
            planet_fleet_statuses[planet.id] = {"inbound_fleets": [], "future_troop_count": planet.troop_count}
        for fleet in self.current_state.fleets:
            if fleet.owner.id == self.current_player.id and fleet.destination.id in planet_fleet_statuses:
                planet_fleet_statuses[fleet.destination.id]["inbound_fleets"].append(fleet)
                planet_fleet_statuses[fleet.destination.id]["future_troop_count"] -= fleet.troop_count
                     


        orders = []


        for planet in self.own_planets:
            sorted_non_friendly_planets = sorted(self.neutral_planets + self.enemy_planets, key= lambda x: get_distance(planet.position, x.position))
            available_troops = planet.troop_count
            i = 0
            while available_troops > 0 and i < len(sorted_non_friendly_planets):
                enemy_p = sorted_non_friendly_planets[i]
                i+=1
                if planet_fleet_statuses[enemy_p.id]["future_troop_count"] >= 0:
                    if enemy_p.owner:
                        max_fleet_time = max(time_to_travel(x.position, enemy_p.position, Fleet.default_fleet_speed) for x in planet_fleet_statuses[enemy_p.id]["inbound_fleets"] + [planet])
                        troops_to_send = min((planet_fleet_statuses[enemy_p.id]["future_troop_count"] + enemy_p.troop_production_rate * max_fleet_time + 1, available_troops))
                    else:
                        troops_to_send = min(planet_fleet_statuses[enemy_p.id]["future_troop_count"] + 1, available_troops)
                    new_order = {
                        "source": planet,
                        "destination": enemy_p,
                        "troop_count": troops_to_send
                    }
                    orders.append(new_order)
                    available_troops -= troops_to_send
        return orders