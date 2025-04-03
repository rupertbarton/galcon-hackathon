from game.team import Team


class Player:
    player_counter = 0

    def __init__(
        self,
        name: str,
        colour: str,
        get_next_orders,
        team: Team = None,
    ):
        self.colour = colour
        self.name = name
        self.team = team
        self.get_next_orders = get_next_orders

        self.id = f"{Player.player_counter}"
        Player.player_counter += 1

    def to_json(self):
        return self.id

    def to_extended_json(self):
        return {
            "n": self.name,
            "c": self.colour,
            "id": self.id} | ({"t": self.team.to_json()} if self.team else {})
