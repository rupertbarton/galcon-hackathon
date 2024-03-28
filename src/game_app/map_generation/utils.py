from game.coordinates import Coordinates
from polar_coordinates import PolarCoordinates

import math

def convert_polar_to_cartesian(coords: PolarCoordinates):
    x = coords.r * math.cos(math.radians(coords.theta))
    y = coords.r * math.sin(math.radians(coords.theta))

    return Coordinates(x,y)
