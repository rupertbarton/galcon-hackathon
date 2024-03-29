from game.galaxy import Galaxy
from game.player import Player

class AbstractBot():

    def __init__(self):
        self.current_state = Galaxy([], [])
        self.current_player = None

    def is_enemy(self, player: Player):
        if not player:
            return False
        elif player.id == self.current_player.id:
            return True 
        elif player.team == None:
            return False
        elif player.team.id == self.current_player.team.id:
            return True
        else:
            return False


    @property
    def own_planets(self):
        return [planet for planet in self.current_state.planets if planet.owner and planet.owner.id == self.current_player.id]

    @property
    def enemy_planets(self):
        return [planet for planet in self.current_state.planets if self.is_enemy(planet.owner)]
    
    @property
    def ally_planets(self):
        return [planet for planet in self.current_state.planets if not self.is_enemy(planet.owner) and not planet.owner.id == self.current_player.id]

    @property
    def neutral_planets(self):
        return [planet for planet in self.current_state.planets if planet.owner == None]

    def create_orders(self, current_player: Player, current_state: Galaxy):
        self.current_state = current_state
        self.current_player = current_player
        
