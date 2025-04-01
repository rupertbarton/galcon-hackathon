import pytest
from typing import List

from game.planet import Planet
from game.fleet import Fleet
from game.coordinates import Coordinates
from game.player import Player
from game.team import Team

TEAM_ALLY = Team("ally", "red")

PLAYER_1 = Player("p1", "blue", lambda _: [], team=TEAM_ALLY)
PLAYER_2 = Player("p2", "red", lambda _: [])
PLAYER_3 = Player("p3", "yellow", lambda _: [], team=TEAM_ALLY)


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
        (
            [(10, PLAYER_2), (5, PLAYER_1)],
            _create_planet(5, PLAYER_1),
            _create_planet(0, PLAYER_2),
        ),
        (
            [(5, PLAYER_1), (10, PLAYER_2)],
            _create_planet(5, PLAYER_1),
            _create_planet(0, PLAYER_1),
        ),
        (
            [(10, PLAYER_3)],
            _create_planet(0, PLAYER_1),
            _create_planet(10, PLAYER_1),
        ),
        (
            [(10, PLAYER_3), (20, PLAYER_2), (15, PLAYER_3)],
            _create_planet(0, PLAYER_1),
            _create_planet(5, PLAYER_3),
        ),
        (
            [(10, PLAYER_3), (30, PLAYER_2), (15, PLAYER_3)],
            _create_planet(0, PLAYER_1),
            _create_planet(5, PLAYER_2),
        ),
    ],
)
def test_combat(
    inbound_fleets: List[Fleet], initial_planet: Planet, expected_final_planet: Planet
):
    initial_planet.arriving_fleets = [
        _create_fleet(*fleet, destination=initial_planet) for fleet in inbound_fleets
    ]

    initial_planet.calculate_combat()
    assert initial_planet.owner == expected_final_planet.owner
    assert initial_planet.troop_count == expected_final_planet.troop_count
    assert initial_planet.arriving_fleets == []


@pytest.mark.parametrize(
    "initial_planet,expected_final_planet",
    [
        (_create_planet(5, PLAYER_1, 5), _create_planet(10, PLAYER_1, 5)),
        (_create_planet(5, None, 5), _create_planet(5, None, 5)),
    ],
)
def test_run(initial_planet: Planet, expected_final_planet: Planet):

    initial_planet.iterate()
    assert initial_planet.owner == expected_final_planet.owner
    assert initial_planet.troop_count == expected_final_planet.troop_count
