import pytest
from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from game.fleet import Fleet
from game.order import Order
from game.team import Team
from game.coordinates import Coordinates
from game.game import Game
from game.utils import get_next_fleet_coords, get_distance

from typing import List

TEAM_ALLY = Team("ally", "red")
TEAM_ENEMY = Team("enemy", "red")

PLAYER_1 = Player("p1", "blue", lambda *_: [])
PLAYER_2 = Player("p2", "red", lambda *_: [])
PLAYER_OG_TEAM = Player("p3", "blue", lambda *_: [], TEAM_ALLY)
PLAYER_ALLY = Player("p4", "blue", lambda *_: [], TEAM_ALLY)
PLAYER_ENEMY = Player("p5", "red", lambda *_: [], TEAM_ENEMY)


def _create_planet(troop_count, player):
    return Planet(Coordinates(0, 0), 2, 0, troop_count, owner=player)


def _create_fleet(troop_count, player, speed=0):
    return Fleet(Coordinates(10, 10), _create_planet(0, None), troop_count, speed, player)


@pytest.mark.parametrize(
    "galaxy,expected_winners,all_players",
    [
        (Galaxy([_create_planet(10, PLAYER_1), _create_planet(5, PLAYER_2)]), {PLAYER_1}, None),
        (Galaxy([_create_planet(10, PLAYER_1), _create_planet(10, PLAYER_2)]), {PLAYER_1, PLAYER_2}, None),
        (Galaxy([_create_planet(10, PLAYER_1), _create_planet(15, None)]), {PLAYER_1}, None),
        (Galaxy([_create_planet(10, PLAYER_1)], [_create_fleet(20, PLAYER_2)]), {PLAYER_2}, None),
        (Galaxy([_create_planet(20, PLAYER_1)], [_create_fleet(10, PLAYER_2)]), {PLAYER_1}, None),
        (Galaxy([], [_create_fleet(10, PLAYER_2)]), {PLAYER_2}, None),
        (Galaxy([_create_planet(20, PLAYER_1), _create_planet(15, PLAYER_2)], [_create_fleet(10, PLAYER_2)]), {PLAYER_2}, None),

        (Galaxy([_create_planet(10, PLAYER_OG_TEAM), _create_planet(5, PLAYER_ENEMY)]), {PLAYER_OG_TEAM, PLAYER_ALLY}, [PLAYER_OG_TEAM, PLAYER_ALLY, PLAYER_ENEMY]),
        (Galaxy([_create_planet(5, PLAYER_OG_TEAM), _create_planet(10, PLAYER_ENEMY)]), {PLAYER_ENEMY}, [PLAYER_OG_TEAM, PLAYER_ALLY, PLAYER_ENEMY]),
    ],
)
def test_winners(
    galaxy: Galaxy, expected_winners: List[Player], all_players: List[Player]
):
    if all_players is None:
        all_players = [PLAYER_1, PLAYER_2]

    actual_winners = Game(all_players, galaxy, max_turn_limit=1).run()
    assert {winner.id for winner in actual_winners} == {winner.id for winner in expected_winners}


TARGET_PLANET = _create_planet(10, PLAYER_1)


@pytest.mark.parametrize(
    "galaxy,max_turn_limit,expected_number_of_times",
    [
        (Galaxy([_create_planet(10, PLAYER_1), _create_planet(10, PLAYER_2)]), 10, 10),
        (Galaxy([TARGET_PLANET], fleets=[Fleet(Coordinates(10, 0), TARGET_PLANET, 20, 2, PLAYER_2)]), 100, 5),
    ],
)
def test_game_end_correctly(galaxy: Galaxy, max_turn_limit: int, expected_number_of_times: int):
    game = Game(list({troop.owner for troop in galaxy.planets + galaxy.fleets if troop.owner}), galaxy, max_turn_limit=max_turn_limit)

    game.run()

    # +1 as initial state is also in history
    assert len(game.history) is expected_number_of_times + 1


def test_orders_can_be_submitted():
    PLAYER_1_PLANET = Planet(Coordinates(10, 0), 2, 0, 10, owner=PLAYER_1)
    PLAYER_ATTACKER_PLANET = Planet(Coordinates(-10, 0), 2, 0, 100, owner=None)
    PLAYER_ATTACKER = Player("p6", "red", lambda _, current_state: [{
        "source": current_state.planets[1],
        "destination": current_state.planets[0],
        "troop_count": 100
    }])
    PLAYER_ATTACKER_PLANET.owner = PLAYER_ATTACKER

    game = Game([PLAYER_1, PLAYER_ATTACKER], Galaxy([PLAYER_1_PLANET, PLAYER_ATTACKER_PLANET]), max_turn_limit=10)
    game.run()
    assert game.winners.pop().id is PLAYER_ATTACKER.id
    assert len(game.history) < 100
