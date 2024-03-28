from planet import Planet
from player import Player

class Order:
    order_count = 0
    def __init__(
        self,
        source: Planet,
        destination: Planet,
        troop_count: int,
        player: Player
    ):
        self.source=source
        self.destination=destination
        self.troop_count=troop_count
        self.player=player
        self.id = f"Order{Order.order_count}"
        Order.order_count += 1
