import pytest
from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from game.fleet import Fleet
from game.order import Order
from game.coordinates import Coordinates
from game.game import Game
from game.utils import get_next_fleet_coords, get_distance

from typing import List
import copy
import logging
import sys

PLAYER_1 = Player("p1", "blue", lambda *_: [])
PLAYER_2 = Player("p2", "red", lambda *_: [])


def _create_planet(troop_count, player):
    return Planet(Coordinates(0, 0), 5, 0, troop_count, owner=player)


def _create_fleet(troop_count, player, speed=0):
    return Fleet(Coordinates(10, 10), _create_planet(0, None), troop_count, speed, player)


@pytest.mark.parametrize(
    "galaxy,expected_winner",
    [
        (Galaxy([_create_planet(10, PLAYER_1), _create_planet(5, PLAYER_2)]), PLAYER_1),
        (Galaxy([_create_planet(10, PLAYER_1), _create_planet(15, None)]), PLAYER_1),
        (Galaxy([_create_planet(10, PLAYER_1)], [_create_fleet(20, PLAYER_2)]), PLAYER_2),
        (Galaxy([_create_planet(20, PLAYER_1)], [_create_fleet(10, PLAYER_2)]), PLAYER_1),
        (Galaxy([], [_create_fleet(10, PLAYER_2)]), PLAYER_2),
        (Galaxy([_create_planet(20, PLAYER_1), _create_planet(15, PLAYER_2)], [_create_fleet(10, PLAYER_2)]), PLAYER_2),

    ],
)
def test_winner(
    galaxy: Galaxy, expected_winner: Player
):

    actual_winner = Game([PLAYER_1, PLAYER_2], galaxy, max_turn_limit=1).run()
    assert actual_winner.id == expected_winner.id
