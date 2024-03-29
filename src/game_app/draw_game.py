from game.galaxy import Galaxy

import matplotlib.pyplot as plt
from typing import List


def draw_galaxy(galaxy: Galaxy, ax=plt.subplots(figsize=(5, 2.7), layout="constrained")):
    planet_data = {
        "x": [planet.position.x for planet in galaxy.planets],
        "y": [planet.position.y for planet in galaxy.planets],
        "s": [planet.radius for planet in galaxy.planets],
        "c": [planet.owner.colour if planet.owner else "grey" for planet in galaxy.planets]
    }

    fleet_data = {
        "x": [fleet.position.x for fleet in galaxy.fleets],
        "y": [fleet.position.y for fleet in galaxy.fleets],
        "c": [fleet.owner.colour if fleet.owner else "grey" for fleet in galaxy.fleets]
    }

    ax.cla()

    ax.scatter("x", "y", c="c", data=planet_data)
    ax.scatter("x", "y", c="c", data=fleet_data)
    ax.set_xlabel("entry x")
    ax.set_ylabel("entry y")

    plt.draw()

def draw_game(history: List[Galaxy], time_per_frame=0.1):
    ax = plt.axes()

    for galaxy in history:
        draw_galaxy(galaxy, ax)
        plt.pause(time_per_frame) #is necessary for the plot to update for some reason
