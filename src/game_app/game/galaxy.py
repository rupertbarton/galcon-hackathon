from game.fleet import Fleet
from game.planet import Planet

from typing import List


class Galaxy:
    def __init__(
        self,
        planets: List[Planet],
        fleets: List[Fleet] = None,
    ):
        if fleets is None:
            fleets = []
        self.planets = planets
        self.fleets = fleets

    def to_json(self):
        return {
            "planets": [planet.to_json() for planet in self.planets],
            "fleets": [fleet.to_json() for fleet in self.fleets],
        }
