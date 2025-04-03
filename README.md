# Galcon

## Instructions to run a game

The main.py file located in `src/game_app` is the entrypoint into the app. Modify this to configure the bots and game configuration you want.

To run the game, first you need to have a virtual environment set up:

```bash
cd src/game_app
python -m venv .venv
source .venv/Scripts/activate
```

[!NOTE] Depending on the vbersion of venv, the activate script may be named differently, see https://docs.python.org/3/library/venv.html

Install dependencies with:

```bash
pip install -r requirements.txt
```

And then to run the game, run:

```bash
python main.py
```

The winner of the game should be printed out to the console, and a file called `{GAME_NAME}.json.gzip` should be created which contains data about the played game.

## How to visualise a game

In `src/game_app/game_draw/run_server.py` lies the code that starts up a local server that enables recordings to be viewed in a browser.

While the virtual environment is active, run `run_server.py` with:

```bash
python src/game_app/game_draw/run_server.py
```

And then in a browser navigate to `http://localhost:8000 and select whichever saved recording you want to view.

You can also navigate to a recording directly by going to the following url, passing a query parameter of the saved recording you would like to view, eg:

```
http://localhost:8000/game_draw/browser_display.html?f=ExampleGame
```

## Creating a bot

`src/game_app/bots` contains several examples bots, but atg it's simplest all it needs to be is a function that takes in 2 arguments: 

1. Current player, which is an object of the Player class, which can be found [here](src/game_app/game/player.py). This object represents the player that your bot controls. Any fleets or planets that have this player as the owner will belong to your bot.
2. Current state, which is an object of the Galaxy class, which can be found [here](src/game_app/game/galaxy.py). This is split into 2 lists of objects:
    1. [Planets](src/game_app/game/planet.py). These are where your troops are made. At the start of the game, each player controls a number of planets, and there are a number of neutral planets. Planets owned by a player generate troops at a rate equal to their `troop_production_rate`. Troops can be ordered to leave a planet, at which point the specified number of troops are converted into a fleet.
    2. [Fleets](src/game_app/game/fleet.py). These are troops in transit between 2 planets. They travel at a certain speed, and they cannot be ordered to change their course.

The function you create needs to return a list of new orders. The structure of an order looks like:

```python
{
    "source": str,
    "destination": str,
    "troop_count": int,
}
```

where:

- Source is the ID of the source planet
- Destination is the ID of the target planet
- troop_count is the number of troops to send to the target planet

A fleet will fail to be created if:

- The player does not own the source planet.
- The number of troops requested excedes the number of troops currently on the source planet.
- If either the source or destination planet does not exist

An [abstract_bot](src/game_app/bots/abstract_bot.py) has been created which can be extended, and has lots of utility functions that can be used to make the process of writing a bot easier.