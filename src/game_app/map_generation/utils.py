from game.coordinates import Coordinates
from map_generation.polar_coordinates import PolarCoordinates

import math


def convert_polar_to_cartesian(coords: PolarCoordinates):
    x = round(coords.r * math.cos(math.radians(coords.theta)), 2)
    y = round(coords.r * math.sin(math.radians(coords.theta)), 2)

    return Coordinates(x, y)
