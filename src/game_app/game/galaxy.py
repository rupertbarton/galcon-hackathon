from game.fleet import Fleet
from game.planet import Planet

from typing import List


class Galaxy:
    def __init__(
        self,
        planets: List[Planet],
        fleets: List[Fleet],
    ):
        self.planets = planets
        self.fleets = fleets
