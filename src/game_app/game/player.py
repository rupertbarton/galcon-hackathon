from game.team import Team

class Player:
    player_counter = 0
    def __init__(
        self,
        name: str,
        colour: str,
        team: Team=None,
    ):
        self.colour=colour
        self.name=name
        self.team=team
        self.id = f"Player{Player.player_counter}"
        Player.player_counter += 1
