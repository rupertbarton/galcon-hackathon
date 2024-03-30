from game.coordinates import Coordinates
from game.utils import get_distance_and_dx_dy

import math

def calculate_direction_angle(start: Coordinates, end: Coordinates):
    _, dx, dy = get_distance_and_dx_dy(start, end)

    angle = math.atan(dy/dx)
    return angle