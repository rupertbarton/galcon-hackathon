import random

from src.game_app.bots.abstract_bot import AbstractBot
from src.game_app.bots.utils import time_to_travel
from src.game_app.game.fleet import Fleet
from src.game_app.game.galaxy import Galaxy
from src.game_app.game.planet import Planet
from src.game_app.game.player import Player
from src.game_app.game.utils import get_distance


class DalesBot(AbstractBot):

    MINIMUM_TROOP_COUNT = 10

    def __init__(self):
        super().__init__()

    def create_orders(self, current_player: Player, current_state: Galaxy):
        super().create_orders(current_player, current_state)
        orders = []

        planets_to_defend, supporting_planets = self.categorise_own_planets()
        troops_about_to_depart = self.defend_planets(orders, planets_to_defend, supporting_planets)

        self.attack_planets(orders, supporting_planets, troops_about_to_depart)

        return orders

    def defend_planets(self, orders, planets_to_defend, supporting_planets):
        planets_to_defend_by_production_desc = sorted(
            planets_to_defend,
            key=lambda x: x.troop_production_rate,
            reverse=True,
        )

        troops_about_to_depart = {planet.id: 0 for planet in self.own_planets}
        for planet_to_defend in planets_to_defend_by_production_desc:
            troops_still_needed = self.MINIMUM_TROOP_COUNT - self.future_troop_count(planet_to_defend)
            supporting_planets_by_distance_desc = sorted(
                supporting_planets,
                key=lambda x: get_distance(planet_to_defend.position, x.position),
                reverse=True,
            )
            for supporting_planet in supporting_planets_by_distance_desc:
                if troops_still_needed <= 0:
                    break

                troops_available = self.calc_troops_available(supporting_planet, troops_about_to_depart)
                troops_to_send = min(troops_available, troops_still_needed)
                orders.append(
                    {
                        "source": supporting_planet.id,
                        "destination": planet_to_defend.id,
                        "troop_count": troops_to_send,
                    }
                )
                troops_still_needed = - troops_to_send
                troops_about_to_depart[supporting_planet.id] += troops_to_send
        return troops_about_to_depart

    def calc_troops_available(self, supporting_planet, troop_count_about_to_depart):
        return min(supporting_planet.troop_count,
                   self.future_troop_count(supporting_planet) - self.MINIMUM_TROOP_COUNT -
                   troop_count_about_to_depart[supporting_planet.id])

    def count_spare_troops(self, planet):
        return self.future_troop_count(planet) - self.MINIMUM_TROOP_COUNT

    def categorise_own_planets(self):
        planets_to_defend = []
        supporting_planets = []
        for planet in self.own_planets:
            if self.future_troop_count(planet) < self.MINIMUM_TROOP_COUNT:
                planets_to_defend.append(planet)
            elif self.future_troop_count(planet) > self.MINIMUM_TROOP_COUNT:
                # Could only attack if number of current troops is higher than total enemy incoming troops
                supporting_planets.append(planet)

        return planets_to_defend, supporting_planets

    def future_troop_count(self, planet: Planet):
        future_troops = planet.troop_count
        for fleet in self.current_state.fleets:
            if fleet.destination.id == planet.id:
                if self.is_enemy_player(fleet.owner):
                    future_troops -= fleet.troop_count
                else:
                    future_troops += fleet.troop_count

        return future_troops

    def attack_planets(self, orders, attacking_planets, troops_about_to_depart):
        # total_attack_force = 0
        # for planet in attacking_planets:
        #     total_attack_force += self.calc_troops_available(planet, troops_about_to_depart)

        targets = self.enemy_planets + self.neutral_planets
        if len(targets) == 0:
            return

        planet_to_attack = random.choice(targets)

        for attacking_planet in attacking_planets:
            attacking_troops = self.calc_troops_available(attacking_planet, troops_about_to_depart)
            orders.append(
                {
                    "source": attacking_planet.id,
                    "destination": planet_to_attack.id,
                    "troop_count": attacking_troops,
                }
            )