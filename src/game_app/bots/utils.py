from game.utils import get_distance
from game.planet import Planet
from game.coordinates import Coordinates

import math
from typing import List

def find_nearest_planet(Coord: Coordinates, planets: List[Planet],):
    closest_planet = planets[0]
    closest_distance = get_distance(Coord, planets[0].position)

    for planet in planets[1:]:
        current_distance = get_distance(Coord, planet.position)
        if current_distance < closest_distance:
            closest_distance = current_distance
            closest_planet = planet
    return closest_planet

def find_nearest_planet_to_a_planet(planet: Planet, planets: List[Planet]):
    return find_nearest_planet(planet.position, planets)

def time_to_travel(start: Coordinates, end: Coordinates, speed: float):
    distance = get_distance(start, end)
    return math.ceil(distance/speed)