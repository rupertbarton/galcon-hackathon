from game.coordinates import Coordinates
from game.planet import Planet
from game.player import Player
from game.utils import get_next_fleet_coords


class Fleet:
    fleet_counter = 0
    default_fleet_speed = 0.3

    def __init__(
        self,
        position: Coordinates,
        destination: Planet,
        troop_count: int,
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

    def move(self):
        self.position = get_next_fleet_coords(
            self.position, self.destination.position, self.speed
        )

    def to_json(self):
        return {
            "p": self.position.to_json(),
            # "destination": self.destination.to_json(),
            "t": self.troop_count,
            # "speed": self.speed,
            "o": self.owner.to_json(),
            # "id": self.id
        }

    def deep_copy(self):
        return Fleet(
            self.position,
            self.destination,
            self.troop_count,
            self.speed,
            self.owner,
        )