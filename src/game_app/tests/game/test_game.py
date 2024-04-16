from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from game.fleet import Fleet
from game.order import Order
from game.game import Game
from game.utils import get_next_fleet_coords, get_distance

from typing import List
import copy
import logging
import sys

PLAYER_1 = Player("p1", "blue", lambda _: [])
PLAYER_2 = Player("p2", "red", lambda _: [])

game = Game([PLAYER_1, PLAYER_2], starting_map.planets, max_turn_limit=1000)