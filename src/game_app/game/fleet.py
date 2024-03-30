from game.coordinates import Coordinates
from game.planet import Planet
from game.player import Player

class Fleet:
    fleet_counter = 0

    def __init__(
        self,
        position: Coordinates,
        destination: Planet,
        troop_count,
        speed=0.7,
        owner: Player=None,
    ):
        self.position=position
        self.destination=destination
        self.troop_count=troop_count
        self.speed=speed
        self.owner=owner
        self.id = f"F{Fleet.fleet_counter}"
        Fleet.fleet_counter += 1
