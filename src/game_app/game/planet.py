from game.coordinates import Coordinates
from game.player import Player
from game.utils import get_time_for_fleet_to_arrive, is_fleet_reinforcing


class Planet:
    planet_counter = 0

    def __init__(
        self,
        position: Coordinates,
        radius: int | float,
        troop_production_rate: int | float,
        troop_count: int | float,
        owner: Player = None,
    ):
        self.position = position
        self.radius = radius
        self.troop_production_rate = troop_production_rate
        self.troop_count = troop_count
        self.owner = owner
        self.arriving_fleets = []
        self.id = f"P{Planet.planet_counter}"
        Planet.planet_counter += 1

    def iterate(self):
        if not self.owner == None:
            self.troop_count += self.troop_production_rate

    def calculate_combat(self):
        self.arriving_fleets.sort(key=get_time_for_fleet_to_arrive)
        for fleet in self.arriving_fleets[:]:
            if is_fleet_reinforcing(fleet):
                self.troop_count += fleet.troop_count
            else:
                self.troop_count -= fleet.troop_count

            if self.troop_count < 0:
                self.owner = fleet.owner
                self.troop_count = abs(self.troop_count)
            self.arriving_fleets.remove(fleet)

    def to_json(self):
        return {
            "p": self.position.to_json(),
            "r": self.radius,
            "t": self.troop_count,
            # "troop_production_rate": self.troop_production_rate,
            "o": self.owner.to_json() if self.owner else None,
            # "id": self.id
        }

    def deep_copy(self):
        return Planet(
            self.position,
            self.radius,
            self.troop_production_rate,
            self.troop_count,
            self.owner,
        )