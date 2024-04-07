import argparse
import random
import socket
import string
from threading import Thread

import numpy as np
from utils import *

# Globals
games = {}


def generate_id():
    return "".join(random.choices(string.digits, k=6))


def handle_client(conn, addr):
    obj = recv(conn)

    if not isinstance(obj, dict) or "type" not in obj:
        print(f"{addr}: Invalid message")
        return

    print(f"{addr}: {obj['type']}")

    if obj["type"] == "echo":
        send(conn, obj["echo"])

    elif obj["type"] in ("new_game", "join_game"):
        if obj["type"] == "new_game":
            game_id = generate_id()
            games[game_id] = Game()
            game = games[game_id]
            game.osm = obj["osm"]
            game.num_players = obj["num_players"]
            game.num_robbers = obj["num_robbers"]
            game.num_helis = obj["num_helis"]
            game.num_cops = game.num_players - game.num_robbers - game.num_helis
            game.generate_targets(obj["num_targets"])
        else:
            game_id = obj["game_id"]
            if game_id not in games:
                send(conn, {"success": False})
                return
            game = games[game_id]

        player_id = generate_id()
        player_type = random.choice(game.remaining_player_types())
        game.players[player_id] = Player(player_id, player_type)

        send(conn, {"success": True, "game_id": game_id, "player_id": player_id, "type": player_type})

    elif obj["type"] == "game_started":
        game = games[obj["game_id"]]
        send(conn, {"started": len(game.players) == game.num_players})

    elif obj["type"] == "game_metadata":
        game = games[obj["game_id"]]
        send(conn, {
            "osm": game.osm,
            "num_players": game.num_players,
            "num_robbers": game.num_robbers,
        })

    elif obj["type"] == "game_state":
        game = games[obj["game_id"]]
        player = game.players[obj["player_id"]]
        player.pos = obj["pos"]
        player.vel = obj["vel"]

        send(conn, {
            "players": game.players,
            "alerts": game.alerts,
            "targets": [x.pos for x in game.targets.values()],
        })

        # Trigger false alert with probability.
        if random.random() < 0.005:
            road = game.osm.get_rand_road()
            if "name" in road.tags:
                game.alerts.append(f"Alert on: {road.tags['name']}")

    elif obj["type"] == "add_alert":
        game = games[obj["game_id"]]
        game.alerts.append(obj["alert"])

    elif obj["type"] == "rob":
        game = games[obj["game_id"]]
        pos = np.array(obj["pos"])

        to_remove = []
        for key, target in game.targets.items():
            if np.linalg.norm(target.pos - pos) < 0.001:
                to_remove.append(key)
        for key in to_remove:
            target = game.targets.pop(key)
            road = target.street
            if "name" in road.tags:
                game.alerts.append(f"Alert on: {target.street.tags['name']}")
            else:
                game.alerts.append("Alert on: Unknown")

        send(conn, {"success": True})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--port", type=int, default=4570)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((args.host, args.port))
    sock.listen()
    print(f"Listening on {args.host}:{args.port}")

    while True:
        conn, addr = sock.accept()
        Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    main()
