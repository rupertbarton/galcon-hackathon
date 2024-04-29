from game.utils import get_time_for_fleet_to_arrive, is_fleet_reinforcing
from game.planet import Planet
from game.fleet import Fleet
from game.player import Player
from game.team import Team

import pytest


# def get_next_fleet_coords(
#     start: Coordinates, end: Coordinates, speed: int
# ) -> Coordinates:

#     total_distance, dx, dy = get_distance_and_dx_dy(start, end)

#     if total_distance == 0:
#         return end

#     fraction_travelled = speed / total_distance

#     if fraction_travelled >= 1:
#         return end

#     final_x = start.x + (dx * fraction_travelled)
#     final_y = start.y + (dy * fraction_travelled)

#     return Coordinates(final_x, final_y)


# def get_distance_and_dx_dy(start: Coordinates, end: Coordinates):
#     dx = end.x - start.x
#     dy = end.y - start.y

#     total_distance = math.sqrt(dx**2 + dy**2)

#     return (total_distance, dx, dy)


# def get_distance(start: Coordinates, end: Coordinates):
#     return get_distance_and_dx_dy(start, end)[0]


# def get_time_for_fleet_to_arrive(fleet):
#     distance = get_distance(fleet.position, fleet.destination.position)
#     time = distance / fleet.speed
#     return time


# def is_fleet_reinforcing(fleet):
#     if fleet.destination.owner == None:
#         return False
#     elif fleet.owner.id == fleet.destination.owner.id:
#         return True
#     elif fleet.owner.team == None or fleet.destination.owner == None:
#         return False
#     elif fleet.owner.team.id == fleet.destination.owner.team.id:
#         return True
#     else:
#         return False

TEAM_ALLY = Team("ally", "red")
TEAM_ENEMY = Team("enemy", "red")


PLAYER_1 = Player("p1", "red", lambda _: [])
PLAYER_2 = Player("p2", "red", lambda _: [])
PLAYER_OG_TEAM = Player("p3", "red", lambda _: [], TEAM_ALLY)
PLAYER_ALLY = Player("p4", "red", lambda _: [], TEAM_ALLY)
PLAYER_ENEMY = Player("p5", "red", lambda _: [], TEAM_ENEMY)


@pytest.mark.parametrize(
    "fleet_owner,destination_owner,expected",
    [
        (PLAYER_1, PLAYER_1, True),
        (PLAYER_1, PLAYER_2, False),
        (PLAYER_1, None, False),
        (PLAYER_OG_TEAM, PLAYER_OG_TEAM, True),
        (PLAYER_OG_TEAM, PLAYER_ALLY, True),
        (PLAYER_OG_TEAM, PLAYER_ENEMY, False),
        (PLAYER_OG_TEAM, None, False),
        (PLAYER_OG_TEAM, PLAYER_1, False),
        (PLAYER_1, PLAYER_OG_TEAM, False),
        (PLAYER_2, PLAYER_1, False),
        (PLAYER_ALLY, PLAYER_OG_TEAM, True),
        (PLAYER_ENEMY, PLAYER_OG_TEAM, False),
    ],
)
def test_is_fleet_reinforcing(fleet_owner, destination_owner, expected):
    destination = Planet(None, None, None, None, owner=destination_owner)

    fleet = Fleet(None, destination, None, None, fleet_owner)

    actual = is_fleet_reinforcing(fleet)

    assert actual == expected
