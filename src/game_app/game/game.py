from game.galaxy import Galaxy
from game.player import Player
from game.planet import Planet
from game.fleet import Fleet
from game.order import Order
from game.utils import get_next_fleet_coords, get_distance

from typing import List, Set
import copy
import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%a, %d %b %Y %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class Game:
    game_counter = 0

    def __init__(
        self,
        players: list[Player],
        starting_map: Galaxy = None,
        history: List[Galaxy] = None,
        max_turn_limit: int = 500,
    ):
        if not starting_map and not history:
            raise ValueError(
                "Either a starting_map or history arg must be passed to a Game"
            )
        elif starting_map and history:
            raise ValueError(
                "Can't specify both a starting_map or history arg for a Game"
            )

        self.players = players

        if starting_map:
            self.current_state = starting_map
            self.history = [self.current_state.deep_copy()]
        else:
            self.history = history
            self.current_state = self.history[-1].deep_copy()
        self.winners: Set[Player] = set()
        self.max_turn_limit = max_turn_limit
        self.finished = False
        self.id = f"G{Game.game_counter}"
        self.planet_dict = {planet.id: planet for planet in self.current_state.planets}
        Game.game_counter += 1

    def _get_player_orders(self) -> List[Order]:
        all_orders = []
        for player in self.players:
            current_p_orders = []

            # TODO: Add timeout to kill bots that hang
            for p_order in player.get_next_orders(player, self.current_state):
                try:
                    source = self.planet_dict[p_order["source"]]
                    destination = self.planet_dict[p_order["destination"]]
                    troop_count = p_order["troop_count"]
                    current_p_orders.append(
                        Order(source, destination, troop_count, player=player)
                    )
                except Exception as e:
                    logger.warning(f"Invalid order passed: {p_order} : {e}")
            all_orders += current_p_orders

        return all_orders

    def _iterate_planets(self):
        for planet in self.current_state.planets:
            planet.iterate()

    def _save_state(self):
        # self.history.append(copy.deepcopy(self.current_state))
        self.history.append(self.current_state.deep_copy())


    def _create_fleets(self, orders: List[Order]):
        for order in orders:
            if self._is_order_valid(order):
                starting_coordinates = get_next_fleet_coords(
                    order.source.position,
                    order.destination.position,
                    order.source.radius,
                )
                troop_count = min(order.troop_count, order.source.troop_count)
                if troop_count > 0:
                    new_fleet = Fleet(
                        position=starting_coordinates,
                        destination=order.destination,
                        troop_count=troop_count,
                        owner=order.player,
                    )
                    order.source.troop_count -= troop_count
                    self.current_state.fleets.append(new_fleet)

    def _is_order_valid(self, order: Order):
        if order.source.owner == None:
            logger.error(
                f"Player {order.player.name} just tried to create an order from a planet they do not own"
            )
            return False
        if not order.player.id == order.source.owner.id:
            logger.error(
                f"Player {order.player.name} just tried to create an order from a planet they do not own"
            )
            return False
        if order.troop_count > order.source.troop_count:
            logger.warning(
                f"Player {order.player.name} just tried to create an order with more troops than are available"
            )
            return False
        return True

    def _move_fleets(self):
        for fleet in self.current_state.fleets:
            if (
                get_distance(fleet.position, fleet.destination.position)
                < fleet.speed + fleet.destination.radius
            ):
                fleet.destination.arriving_fleets.append(fleet)
                self.current_state.fleets.remove(fleet)
            else:
                fleet.move()

    def _calculate_combat(self):
        for planet in self.current_state.planets:
            if planet.arriving_fleets:
                planet.calculate_combat()

    def _check_for_end(self):
        remaining_player_ids = set()

        for troops in self.current_state.planets + self.current_state.fleets:
            if troops.owner:
                remaining_player_ids.add(troops.owner.id)
        if len(remaining_player_ids) <= 1:
            self.finished = True

        remaining_players = filter(
            lambda player: player.id in remaining_player_ids, self.players
        )
        if (
            all([player.team for player in remaining_players])
            and len(set([player.team.id for player in remaining_players])) <= 1
        ):
            self.finished = True

    def _calculate_winners(self):
        troops_counts = {
            player.id: {"player": player, "count": 0} for player in self.players
        }
        for troops in self.current_state.planets + self.current_state.fleets:
            if troops.owner:
                troops_counts[troops.owner.id]["count"] += troops.troop_count
        current_winner = max(troops_counts.values(), key=lambda p: p["count"])

        self.winners.add(current_winner["player"])

        self.winners.update(
            [
                count["player"]
                for count in troops_counts.values()
                if count["count"] == current_winner["count"]
            ]
        )

        # Calculate winners due to being on the winning team

        team_winners = set()
        for winner in self.winners:
            for player in self.players:
                if winner.team and player.team and winner.team.id == player.team.id:
                    team_winners.add(player)
        self.winners.update(team_winners)

    def run(self):
        while not self.finished and len(self.history) <= self.max_turn_limit:
            orders = self._get_player_orders()
            self._move_fleets()
            self._create_fleets(orders)
            self._calculate_combat()
            self._iterate_planets()
            self._check_for_end()
            self._save_state()
            print(len(self.history))
        self._calculate_winners()
        return self.winners

    def to_json(self):
        return {
            "galaxies": [galaxy.to_json() for galaxy in self.history],
            "players": [player.to_extended_json() for player in self.players]
            }
