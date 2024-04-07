import argparse
import time

import pygame
pygame.init()

from game_loop import game_loop
from utils import *


def get_session_id(args) -> tuple[str, str] | None:
    """
    Uses CLI to either start or join game.

    Return: (game_id, player_id)
    """
    print("Would you like to start a new game or join an existing game?")
    print("  1. Start a new game")
    print("  2. Join an existing game")
    choice = input("Enter 1 or 2: ")
    print()

    if choice == "1":
        print("Start game:")
        num_players = int(input("Number of players: "))
        resp = request(args.host, args.port, {"type": "new_game", "num_players": num_players})
        print("  Game ID:", resp["game_id"])
        return resp["game_id"], resp["player_id"]

    elif choice == "2":
        print("Join game:")
        game_id = input("  Game ID: ")
        resp = request(args.host, args.port, {"type": "join_game", "game_id": game_id})
        if resp["success"]:
            return game_id, resp["player_id"]
        else:
            print("Invalid game ID.")

    else:
        print("Invalid choice.")


def wait_for_start(args, game_id):
    print("Waiting for game to start...")
    while True:
        resp = request(args.host, args.port, {"type": "game_started", "game_id": game_id})
        if resp["started"]:
            print("Game started!")
            break
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--port", type=int, default=6645)
    args = parser.parse_args()

    ret = get_session_id(args)
    if ret is None:
        return

    game_id, player_id = ret
    wait_for_start(args, game_id)

    game_loop(args, game_id, player_id)


if __name__ == "__main__":
    main()
