from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from typing import List


class AbstractBot:

    def __init__(self):
        self.current_state = Galaxy([], [])
        self.current_player = None

    def is_enemy_player(self, player: Player)  -> bool:
        if not player:
            return False
        elif player.id == self.current_player.id:
            return False
        elif player.team is None:
            return True
        elif self.current_player.team is None:
            return True
        elif player.team.id == self.current_player.team.id:
            return False
        else:
            return True

    def is_neutral_planet(self, planet: Planet) -> bool:
        if planet.owner == None:
            return True
        else:
            return False

    def is_own_planet(self, planet: Planet) -> bool:
        if planet.owner and planet.owner.id == self.current_player.id:
            return True
        else:
            return False

    def is_friendly_planet(self, planet: Planet) -> bool:
        if not self.is_neutral_planet(planet) and not self.is_enemy_planet(planet):
            return True
        else:
            return False

    def is_enemy_planet(self, planet: Planet) -> bool:
        if not self.is_neutral_planet(planet) and self.is_enemy_player(planet.owner):
            return True
        else:
            return False

    @property
    def all_planets(self) -> List[Planet]:
        return self.current_state.planets

    @property
    def own_planets(self) -> List[Planet]:
        return [
            planet
            for planet in self.current_state.planets
            if self.is_own_planet(planet)
        ]

    @property
    def enemy_planets(self) -> List[Planet]:
        return [
            planet
            for planet in self.current_state.planets
            if self.is_enemy_planet(planet)
        ]

    @property
    def ally_planets(self) -> List[Planet]:
        return [
            planet
            for planet in self.current_state.planets
            if self.is_friendly_planet(planet) and not self.is_own_planet(planet)
        ]

    @property
    def neutral_planets(self) -> List[Planet]:
        return [
            planet
            for planet in self.current_state.planets
            if self.is_neutral_planet(planet)
        ]

    @property
    def friendly_planets(self) -> List[Planet]:
        return [
            planet
            for planet in self.current_state.planets
            if self.is_friendly_planet(planet)
        ]

    def create_orders(self, current_player: Player, current_state: Galaxy):
        self.current_state = current_state
        self.current_player = current_player
