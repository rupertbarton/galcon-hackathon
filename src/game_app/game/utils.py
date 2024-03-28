from coordinates import Coordinates
from fleet import Fleet

from typing import List
import math

def get_next_fleet_coords(start: Coordinates, end: Coordinates, speed: int) -> Coordinates:

    total_distance, dx, dy = get_distance_and_dx_dy(start, end)
    fraction_travelled = speed/total_distance

    if fraction_travelled >= 1:
        return end

    final_x = start.x + (dx*fraction_travelled)
    final_y = start.y + (dy*fraction_travelled)

    return Coordinates(final_x, final_y)

def get_distance_and_dx_dy(start: Coordinates, end: Coordinates):
    dx = end.x - start.x
    dy = end.y - start.y

    total_distance = math.sqrt(dx**2 + dy**2)

    return (total_distance, dx, dy)

def get_distance(start: Coordinates, end: Coordinates):
    return get_distance_and_dx_dy(start, end)[0]

def get_time_for_fleet_to_arrive(fleet: Fleet):
    distance = get_distance(fleet.position, fleet.destination):
    time = distance / fleet.speed
    return time

def is_fleet_reinforcing(fleet: Fleet):
    if fleet.owner is fleet.destination.owner:
        return True
    elif fleet.owner.team is None or fleet.destination.owner is None:
        return False
    elif fleet.owner.team is fleet.destination.owner.team:
        return True