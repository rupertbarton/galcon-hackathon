import pytest
from typing import List

from game.planet import Planet
from game.fleet import Fleet
from game.coordinates import Coordinates
from game.player import Player
from game.team import Team

TEAM_ALLY = Team("ally", "red")
TEAM_ENEMY = Team("enemy", "red")

PLAYER_1 = Player("p1", "blue", lambda _: [], team=TEAM_ALLY)
PLAYER_2 = Player("p2", "red", lambda _: [])

def _create_planet(troop_count, player, troop_production=5):
    return Planet(Coordinates(0, 0), 5, troop_production, troop_count, owner=player)

def _create_fleet(troop_count, player, distance=0, destination=_create_planet(0, None)):
    return Fleet(Coordinates(0, distance), destination, troop_count, 5, player)

@pytest.mark.parametrize(
    "inbound_fleets,initial_planet,expected_final_planet",
    [
        ([], _create_planet(5, PLAYER_1), _create_planet(5, PLAYER_1)),
        ([(5, PLAYER_2)], _create_planet(5, PLAYER_1), _create_planet(0, PLAYER_1)),
        ([(10, PLAYER_2)], _create_planet(5, PLAYER_1), _create_planet(5, PLAYER_2)),
        ([(10, PLAYER_2), (5, PLAYER_1)], _create_planet(5, PLAYER_1), _create_planet(0, PLAYER_2)),
        ([(5, PLAYER_1), (10, PLAYER_2)], _create_planet(5, PLAYER_1), _create_planet(0, PLAYER_1)),
        ],
)
def test_combat(inbound_fleets: List[Fleet], initial_planet: Planet, expected_final_planet: Planet):
    initial_planet.arriving_fleets = [_create_fleet(*fleet, destination=initial_planet) for fleet in inbound_fleets]

    initial_planet.calculate_combat()
    assert initial_planet.owner == expected_final_planet.owner
    assert initial_planet.troop_count == expected_final_planet.troop_count
    assert initial_planet.arriving_fleets == []
    

@pytest.mark.parametrize(
    "initial_planet,expected_final_planet",
    [
        (_create_planet(5, PLAYER_1, 5), _create_planet(10, PLAYER_1, 5)),
    ],
)
def test_run(initial_planet: Planet, expected_final_planet: Planet):

    initial_planet.run()
    assert initial_planet.owner == expected_final_planet.owner
    assert initial_planet.troop_count == expected_final_planet.troop_count


# class Planet:
#     planet_counter = 0

#     def __init__(
#         self,
#         position: Coordinates,
#         radius,
#         troop_production_rate,
#         troop_count,
#         owner: Player = None,
#     ):
#         self.position = position
#         self.radius = radius
#         self.troop_production_rate = troop_production_rate
#         self.troop_count = troop_count
#         self.owner = owner
#         self.arriving_fleets = []
#         self.id = f"P{Planet.planet_counter}"
#         Planet.planet_counter += 1

#     def run(self):
#         if not self.owner == None:
#             self.troop_count += self.troop_production_rate

#     def calculate_combat(self):
#         self.arriving_fleets.sort(key=get_time_for_fleet_to_arrive)
#         for fleet in self.arriving_fleets:
#             if is_fleet_reinforcing(fleet):
#                 self.troop_count += fleet.troop_count
#             else:
#                 self.troop_count -= fleet.troop_count

#             if self.troop_count < 0:
#                 self.owner = fleet.owner
#                 self.troop_count = abs(self.troop_count)
#             self.arriving_fleets.remove(fleet)

#     def to_json(self):
#         return {
#             "position": self.position.to_json(),
#             "radius": self.radius,
#             # "troop_count": self.troop_count,
#             # "troop_production_rate": self.troop_production_rate,
#             "owner": self.owner.to_json() if self.owner else None,
#             # "id": self.id
#         }
