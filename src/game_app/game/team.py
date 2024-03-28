class Team:
    team_counter = 0
    def __init__(
        self,
        name: str,
        colour: str,
    ):
        self.colour=colour
        self.name=name
        self.id = f"Team{Team.team_counter}"
        Team.player_counter += 1
