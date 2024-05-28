

from typing import List

from src.game_app.game.fleet import Fleet
from src.game_app.game.planet import Planet


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

    def deep_copy(self):
        planets = [p.deep_copy() for p in self.planets]
        fleets = [f.deep_copy() for f in self.fleets]
        return Galaxy(planets, fleets)