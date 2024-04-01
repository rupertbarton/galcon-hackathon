from game.coordinates import Coordinates
from game.planet import Planet
from game.player import Player


class Fleet:
    fleet_counter = 0
    default_fleet_speed = 0.3

    def __init__(
        self,
        position: Coordinates,
        destination: Planet,
        troop_count,
        speed=default_fleet_speed,
        owner: Player = None,
    ):
        self.position = position
        self.destination = destination
        self.troop_count = troop_count
        self.speed = speed
        self.owner = owner
        self.id = f"F{Fleet.fleet_counter}"
        Fleet.fleet_counter += 1
