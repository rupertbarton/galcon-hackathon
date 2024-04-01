from game.galaxy import Galaxy
from game_draw.utils import calculate_direction_angle

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import List


def draw_galaxy(galaxy: Galaxy, ax: Axes=plt.subplots(figsize=(5, 2.7), layout="constrained")):

    fleet_data = {
        "x": [fleet.position.x for fleet in galaxy.fleets],
        "y": [fleet.position.y for fleet in galaxy.fleets],
        "c": [fleet.owner.colour if fleet.owner else "grey" for fleet in galaxy.fleets]
    }


    ax.cla()

    for planet in galaxy.planets:
        circ = plt.Circle(
            (planet.position.x, planet.position.y), planet.radius, color=planet.owner.colour if planet.owner else "grey")
        ax.add_patch(circ)

    ax.scatter("x", "y", c="c", data=fleet_data)

    total_troops = {}

    # Add Number label to fleets and planets
    for troops in galaxy.planets + galaxy.fleets:
        ax.annotate(troops.troop_count, (troops.position.x, troops.position.y))
        if troops.owner:
            if not troops.owner.id in total_troops:
                total_troops[troops.owner.id] = {"colour": troops.owner.colour, "troop_count": 0}
            total_troops[troops.owner.id]["troop_count"] += troops.troop_count

    for i, player in enumerate(total_troops):
        ax.text((i-1)*1/len(total_troops), 0.01, total_troops[player]["troop_count"],
                verticalalignment='bottom', horizontalalignment='right',
                # transform=ax.transAxes,
                color=total_troops[player]["colour"], fontsize=12, fontweight='bold')

    plt.draw()

def draw_game(history: List[Galaxy], time_per_frame=0.1):
    ax = plt.axes()
    ax.set_xlim(30)
    ax.set_ylim(30)

    for galaxy in history:
        draw_galaxy(galaxy, ax)
        plt.pause(time_per_frame)
