import random
import time

import numpy as np


def remove_old(games):
    to_remove = []
    for game_id, game in games.items():
        if time.time() - game.last_ping > 10:
            to_remove.append(game_id)

    for game_id in to_remove:
        print(f"Daemon: Removing game {game_id}")
        del games[game_id]


def update_game(game):
    # Trigger false alert with probability.
    if random.random() < 0.003:
        road = game.osm.get_rand_road()
        if "name" in road.tags:
            game.alerts.append(f"{road.tags['name']}")

    # Check if robber is captured.
    robbers = [x for x in game.players.values() if x.type == "robber"]
    cops = [x for x in game.players.values() if x.type == "cop"]
    check_cops_win = False
    for robber in robbers:
        for cop in cops:
            if 1e-7 < np.linalg.norm(robber.pos - cop.pos) < 0.0004:
                robber.type = "spectator"
                game.alerts.append("Robber captured.")
                check_cops_win = True
                break

    # Check if cops win.
    if check_cops_win:
        for player in game.players.values():
            if player.type == "robber":
                break
        else:
            game.alerts.append("Cops win!")


def daemon(games):
    while True:
        time.sleep(0.2)

        try:
            remove_old(games)
            for game in games.values():
                update_game(game)
        except Exception as e:
            print(f"Error in daemon: {e}")
