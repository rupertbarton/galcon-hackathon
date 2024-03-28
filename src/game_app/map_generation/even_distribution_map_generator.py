from game.player import Player
from game.planet import Planet
from polar_coordinates import PolarCoordinates
from abstract_map_generator import AbstractMapGenerator
from utils import convert_polar_to_cartesian

from typing import List

class EvenDistributionMapGenerator(AbstractMapGenerator):

    def create_map(self):
        planet_list = []
        p1_homeworld_coords = PolarCoordinates(self.max_radius, 0)
        all_homeworld_coords = self.get_rotationally_reflect_coords_list(p1_homeworld_coords)

        for i, player in enumerate(self.players):
            new_homeworld_planet = Planet(convert_polar_to_cartesian(all_homeworld_coords[i]), self.size_of_home_planet, self.size_of_home_planet, self.starting_troop_count, player)
            planet_list.append(new_homeworld_planet)

        for _ in range(self.number_of_planets_per_player):
            p1_new_planet_coords = PolarCoordinates(self.max_radius, 0)
            all_new_planet_coords = self.get_rotationally_reflect_coords_list(p1_new_planet_coords)
            new_homeworld_planet = Planet(convert_polar_to_cartesian(all_homeworld_coords[i]), self.size_of_home_planet, self.size_of_home_planet, self.starting_troop_count, player)




        for polar_coord in self.planet_polar_coords:
            new_planet = Planet()
