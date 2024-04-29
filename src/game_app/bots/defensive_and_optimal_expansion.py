from bots.abstract_bot import AbstractBot
from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from game.utils import get_distance
from bots.utils import time_to_travel
from game.fleet import Fleet


class DefensiveAndOptimalExpansionBot(AbstractBot):

    def __init__(self):
        super().__init__()

    def create_orders(self, current_player: Player, current_state: Galaxy):
        super().create_orders(current_player, current_state)

        orders = []

        # Set up dicts
        available_troops = {
            planet.id: planet.troop_count for planet in self.own_planets
        }
        incoming_fleets = {planet.id: [] for planet in self.own_planets}
        planets_dict = {planet.id: planet for planet in self.current_state.planets}
        for fleet in self.current_state.fleets:
            if fleet.destination.owner and fleet.destination.owner.id == self.current_player.id:
                incoming_fleets[fleet.destination.id].append(fleet)
        for planet_id in incoming_fleets:
            for fleet in incoming_fleets[planet_id]:
                if self.is_enemy_player(fleet.owner):
                    available_troops[planet_id] -= fleet.troop_count
                else:
                    available_troops[planet_id] += fleet.troop_count

        # Defend planets that need defending
        for planet_id in available_troops:
            if available_troops[planet_id] < 0:
                sorted_own_planets = sorted(
                    self.own_planets,
                    key=lambda x: get_distance(planets_dict[planet_id].position, x.position),
                )
                for supporting_planet in sorted_own_planets:
                    if available_troops[supporting_planet.id] > 0:
                        troops_to_send = min(
                            abs(available_troops[planet_id]),
                            available_troops[supporting_planet.id],
                        )
                        available_troops[planet_id] += troops_to_send
                        available_troops[supporting_planet.id] -= troops_to_send
                        orders.append(
                            {
                                "source": supporting_planet.id,
                                "destination": planet_id,
                                "troop_count": troops_to_send,
                            }
                        )


        # Copied from optimal expansion bot
        planet_fleet_statuses = {}
        for planet in self.neutral_planets + self.enemy_planets:
            planet_fleet_statuses[planet.id] = {
                "inbound_fleets": [],
                "future_troop_count": planet.troop_count,
            }
        for fleet in self.current_state.fleets:
            if (
                fleet.owner.id == self.current_player.id
                and fleet.destination.id in planet_fleet_statuses
            ):
                planet_fleet_statuses[fleet.destination.id]["inbound_fleets"].append(
                    fleet
                )
                planet_fleet_statuses[fleet.destination.id][
                    "future_troop_count"
                ] -= fleet.troop_count

        for planet in self.own_planets:
            sorted_non_friendly_planets = sorted(
                self.neutral_planets + self.enemy_planets,
                key=lambda x: get_distance(planet.position, x.position),
            )
            current_available_troops = available_troops[planet.id]
            i = 0
            while current_available_troops > 0 and i < len(sorted_non_friendly_planets):
                enemy_p = sorted_non_friendly_planets[i]
                i += 1
                if planet_fleet_statuses[enemy_p.id]["future_troop_count"] >= 0:
                    if enemy_p.owner:
                        max_fleet_time = max(
                            time_to_travel(
                                x.position, enemy_p.position, Fleet.default_fleet_speed
                            )
                            for x in planet_fleet_statuses[enemy_p.id]["inbound_fleets"]
                            + [planet]
                        )
                        troops_to_send = min(
                            (
                                planet_fleet_statuses[enemy_p.id]["future_troop_count"]
                                + enemy_p.troop_production_rate * max_fleet_time
                                + 1,
                                current_available_troops,
                            )
                        )
                    else:
                        troops_to_send = min(
                            planet_fleet_statuses[enemy_p.id]["future_troop_count"] + 1,
                            current_available_troops,
                        )
                    new_order = {
                        "source": planet.id,
                        "destination": enemy_p.id,
                        "troop_count": troops_to_send,
                    }
                    orders.append(new_order)
                    current_available_troops -= troops_to_send


        return orders
