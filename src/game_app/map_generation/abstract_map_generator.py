from game.player import Player
from map_generation.polar_coordinates import PolarCoordinates

from typing import List


class AbstractMapGenerator:

    def __init__(
        self,
        max_radius: int,
        number_of_planets_per_player: int,
        players: List[Player],
        size_of_home_planet: int = 5,
        starting_troop_count: int = 100,
    ):
        self.max_radius = max_radius
        self.number_of_planets_per_player = number_of_planets_per_player
        self.players = players
        self.size_of_home_planet = size_of_home_planet
        self.starting_troop_count = starting_troop_count
        self.planet_polar_coords = []

    def get_rotationally_reflect_coords_list(self, initial_coords: PolarCoordinates):
        final_list_of_coords = [initial_coords]
        d_theta = 360 / len(self.players)
        for i in range(len(self.players) - 1):
            new_coord = PolarCoordinates(
                initial_coords.r, initial_coords.theta + d_theta * (i + 1)
            )
            final_list_of_coords.append(new_coord)
        return final_list_of_coords

    def create_map(self):
        pass
