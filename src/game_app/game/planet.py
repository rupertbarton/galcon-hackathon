from coordinates import Coordinates
from player import Player
from utils import get_time_for_fleet_to_arrive, is_fleet_reinforcing

class Planet:
    planet_counter = 0

    def __init__(
        self,
        position:Coordinates,
        radius,
        troop_production_rate,
        troop_count,
        owner: Player=None,
    ):
        self.position=position
        self.radius=radius
        self.troop_production_rate=troop_production_rate
        self.troop_count=troop_count
        self.owner=owner
        self.arriving_fleets=[]
        self.id = f"P{Planet.planet_counter}"
        Planet.planet_counter += 1
    
    def run(self):
        self.troop_count += self.troop_production_rate

    def calculate_combat(self):
        self.arriving_fleets.sort(key=get_time_for_fleet_to_arrive)
        for fleet in self.arriving_fleets:
            if is_fleet_reinforcing(fleet):
                self.troop_count += fleet.troop_count
            else:
                self.troop_count - fleet.troop_count
            
            if self.troop_count < 0:
                self.owner = fleet.owner
                self.troop_count = abs(self.troop_count)