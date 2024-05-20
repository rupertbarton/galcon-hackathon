from game.galaxy import Galaxy
from game.player import Player


def get_actions_in_state(state: Galaxy):
    
    quantities = [0.25, 0.5, 0.75, 1]
    
    # Empty list for the situation when nno order is chosen
    actions = [[]]
    
    for i in state.planets:
        for j in state.planets:
            for q in quantities:
                actions.append([{"source": i.id, "destination": j.id, "troop_count": i.troop_count * q}])
    
    return actions

def get_observations_in_state(current_player: Player, state: Galaxy):
    observations = [get_int_from_str(current_player.id)]
    
    for planet in state.planets:
        observations.append(get_int_from_str(planet.owner.id) if planet.owner else -1)
        observations.append(planet.position.x)
        observations.append(planet.position.y)
        observations.append(planet.troop_count)
        observations.append(planet.troop_production_rate)
    
    return observations

def get_int_from_str(string: str):
    return int(''.join(filter(str.isdigit, string)))