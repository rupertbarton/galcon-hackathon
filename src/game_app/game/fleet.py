from coordinates import Coordinates
from planet import Planet
from player import Player

class Fleet:
    fleet_counter = 0

    def __init__(
        self,
        position: Coordinates,
        destination: Planet,
        troop_count,
        speed=5,
        owner: Player=None,
    ):
        self.position=position
        self.destination=destination
        self.troop_count=troop_count
        self.speed=speed
        self.owner=owner
        self.id = f"P{Fleet.fleet_counter}"
        Fleet.fleet_counter += 1
