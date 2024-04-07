import random
import time

import numpy as np


def update_game(game):
    # Trigger false alert with probability.
    if random.random() < 0.004:
        road = game.osm.get_rand_road()
        if "name" in road.tags:
            game.alerts.append(f"Alert on: {road.tags['name']}")

    # Check if robber is captured.
    robbers = [x for x in game.players.values() if x.type == "robber"]
    cops = [x for x in game.players.values() if x.type == "cop"]
    for robber in robbers:
        for cop in cops:
            if 1e-7 < np.linalg.norm(robber.pos - cop.pos) < 0.001:
                robber.type = "spectator"
                game.alerts.append("Robber captured.")
                break


def daemon(games):
    while True:
        time.sleep(0.2)

        for game in games.values():
            update_game(game)
