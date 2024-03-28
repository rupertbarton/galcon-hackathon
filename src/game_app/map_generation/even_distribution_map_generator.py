from game.galaxy import Galaxy
from game.planet import Planet
from map_generation.polar_coordinates import PolarCoordinates
from map_generation.abstract_map_generator import AbstractMapGenerator
from map_generation.utils import convert_polar_to_cartesian

import math
import random

class EvenDistributionMapGenerator(AbstractMapGenerator):

    def create_map(self):
        planet_list = []
        p1_homeworld_coords = PolarCoordinates(self.max_radius, 0)
        all_homeworld_coords = self.get_rotationally_reflect_coords_list(p1_homeworld_coords)

        for i, player in enumerate(self.players):
            new_homeworld_planet = Planet(convert_polar_to_cartesian(all_homeworld_coords[i]), self.size_of_home_planet, self.size_of_home_planet, self.starting_troop_count, player)
            planet_list.append(new_homeworld_planet)

        for _ in range(self.number_of_planets_per_player):
            p1_new_planet_coords = PolarCoordinates(self.max_radius*math.sqrt(random.random()), random.random()*360)
            new_planet_size = random.randint(1,self.size_of_home_planet-1)
            new_planet_troop_count = random.randint(1, int(self.starting_troop_count/2))
            all_new_planet_coords = self.get_rotationally_reflect_coords_list(p1_new_planet_coords)
            for i, player in enumerate(self.players):
                new_homeworld_planet = Planet(convert_polar_to_cartesian(all_new_planet_coords[i]), new_planet_size, new_planet_size, new_planet_troop_count)
                planet_list.append(new_homeworld_planet)

        return Galaxy(planet_list, [])