__all__ = (
    "Game",
    "Player",
)

"""
Classes relating to gameplay.
"""

from dataclasses import dataclass

import numpy as np

from .map import OSM


class Game:
    osm: OSM
    players: dict[str, "Player"]
    num_players: int
    num_robbers: int
    num_helis: int
    num_cops: int
    alerts: list[str]
    targets: dict[int, "Target"]

    def __init__(self):
        self.players = {}
        self.alerts = []
        self.targets = {}

    def num_players_of(self, type: str) -> int:
        return sum(1 for player in self.players.values() if player.type == type)

    def remaining_player_types(self) -> list[str]:
        num_cops = self.num_players_of("cop")
        num_helis = self.num_players_of("heli")
        num_robbers = self.num_players_of("robber")
        remain = []
        for _ in range(self.num_robbers - num_robbers):
            remain.append("robber")
        for _ in range(self.num_helis - num_helis):
            remain.append("heli")
        for _ in range(self.num_cops - num_cops):
            remain.append("cop")

        return remain

    def generate_targets(self, num_targets: int):
        for i in range(num_targets):
            street, pos = self.osm.get_rand_road_pos()
            pos = np.array(pos)
            self.targets[i] = Target(pos, street)


class Player:
    id: str
    pos: np.ndarray
    vel: np.ndarray
    type: str

    def __init__(self, id, type):
        self.pos = np.zeros(2)
        self.vel = np.zeros(2)
        self.id = id
        self.type = type


@dataclass
class Target:
    pos: np.ndarray
    street: "Way"
