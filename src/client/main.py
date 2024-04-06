import argparse
import xml.etree.ElementTree as ET
from dataclasses import dataclass

import numpy as np
import pygame
import time

from utils import *


@dataclass
class Node:
    id: int
    lat: float
    lon: float


@dataclass
class Way:
    id: int
    nodes: list[Node]
    tags: dict[str, str]


@dataclass
class OSM:
    nodes: dict[int, Node]
    ways: list[Way]

    # lat and lon bounds
    top: float
    left: float
    bottom: float
    right: float

    scaling_factor: float = 1


class Display:

    WIDTH = 1280
    HEIGHT = 720

    def __init__(self, data):
        self.data = data

    def render(self):
        surface = pygame.Surface((800, 600))
        surface.fill((255, 255, 255))

        for way in self.data.ways:
            for i in range(len(way.nodes) - 1):
                p1 = self.project(way.nodes[i].lat, way.nodes[i].lon)
                p2 = self.project(
                    way.nodes[i + 1].lat, way.nodes[i + 1].lon
                )
                pygame.draw.line(surface, (0, 0, 0), p1, p2, 1)

        return surface

    def project(self, lat, lon):
        x_size = self.WIDTH
        y_size = (
            self.data.scaling_factor
            * x_size
            * (self.data.top - self.data.bottom)
            / (self.data.right - self.data.left)
        )
        x = np.interp(lon, [self.data.left, self.data.right], [-x_size / 2, x_size / 2])
        y = -np.interp(lat, [self.data.top, self.data.bottom], [y_size / 2, -y_size / 2])
        x += self.WIDTH / 2
        y += self.WIDTH / 2
        return x, y


def parse_osm_file(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return parse_osm(root)


def parse_osm(root):
    nodes = {}
    ways = []

    top = float("inf")
    left = float("inf")
    bottom = float("-inf")
    right = float("-inf")

    for child in root:
        if child.tag == "node":
            id = int(child.attrib["id"])
            lat = float(child.attrib["lat"])
            lon = float(child.attrib["lon"])
            nodes[id] = Node(
                id=id,
                lat=lat,
                lon=lon,
            )

            top = min(top, lat)
            left = min(left, lon)
            bottom = max(bottom, lat)
            right = max(right, lon)

        elif child.tag == "way":
            way = Way(
                id=int(child.attrib["id"]),
                nodes=[],
                tags={},
            )
            for subchild in child:
                if subchild.tag == "nd":
                    way.nodes.append(nodes[int(subchild.attrib["ref"])])
                elif subchild.tag == "tag":
                    way.tags[subchild.attrib["k"]] = subchild.attrib["v"]
            ways.append(way)

    # TODO explain this
    scaling = 1 / np.cos(np.radians(top))

    return OSM(
        nodes=nodes,
        ways=ways,
        top=top,
        left=left,
        bottom=bottom,
        right=right,
        scaling_factor=scaling,
    )


def get_session_id(args) -> tuple[str, str]:
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


if __name__ == "__main__":
    main()
