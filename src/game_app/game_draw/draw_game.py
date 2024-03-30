from game.galaxy import Galaxy
from game_draw.utils import calculate_direction_angle

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import List
from matplotlib.animation import FuncAnimation




def draw_game(history: List[Galaxy], time_per_frame=0.1):
    fig = plt.figure(figsize=(10,10))
    ax=plt.axes(xlim=(-10,10),ylim=(-10,10))

    def draw_galaxy(galaxy: Galaxy, layout="constrained"):
        print(galaxy)
        planet_data = {
            "x": [planet.position.x for planet in galaxy.planets],
            "y": [planet.position.y for planet in galaxy.planets],
            "s": [20*2**planet.radius for planet in galaxy.planets],
            "c": [planet.owner.colour if planet.owner else "grey" for planet in galaxy.planets]
        }

        fleet_data = {
            "x": [fleet.position.x for fleet in galaxy.fleets],
            "y": [fleet.position.y for fleet in galaxy.fleets],
            "c": [fleet.owner.colour if fleet.owner else "grey" for fleet in galaxy.fleets]
        }

        actors = []

        for planet in galaxy.planets:
            circ = plt.Circle(
                (planet.position.x, planet.position.y), planet.radius, color=planet.owner.colour if planet.owner else "grey")
            ax.add_patch(circ)
            actors.append(circ)

            planet_text = ax.text(planet.position.x, planet.position.y, planet.troop_count,
                    horizontalalignment='center', verticalalignment='center')
            actors.append(planet_text)


        # ax.scatter("x", "y", s="s", c="c", data=planet_data)
        ax.scatter("x", "y", c="c", data=fleet_data)
        fleets = ax.scatter("x", "y", c="c", data=fleet_data)
        actors.append(fleets)
        total_troops = {}

        # Add Number label to fleets and planets
        for troops in galaxy.planets + galaxy.fleets:
            count_annotation = ax.text(troops.position.x, troops.position.y, troops.troop_count,
                    horizontalalignment='center', verticalalignment='center')
            actors.append(count_annotation)
            if troops.owner:
                if not troops.owner.id in total_troops:
                    total_troops[troops.owner.id] = {"colour": troops.owner.colour, "troop_count": 0}
                total_troops[troops.owner.id]["troop_count"] += troops.troop_count

        # for i, player in enumerate(total_troops):
        #     summary_text = ax.text((i-1)*1/len(total_troops), 0.01, total_troops[player]["troop_count"],
        #             verticalalignment='bottom', horizontalalignment='right',
        #             # transform=ax.transAxes,
        #             color=total_troops[player]["colour"], fontsize=12, fontweight='bold')
        #     actors.append(summary_text)
        # print(actors)
        return actors
    # def update_galaxy(galaxy):
    #     a
    #     for planet in galaxy.planets:
    #         circ = plt.Circle(
    #             (planet.position.x+1, planet.position.y+1), planet.radius, color=planet.owner.colour if planet.owner else "grey")
    #         circles.append(circ)
    #     return circles

    FuncAnimation(fig, draw_galaxy, frames=history, blit=True)

    plt.show()
