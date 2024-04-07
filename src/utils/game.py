__all__ = (
    "Game",
    "Player",
)

"""
Classes relating to gameplay.
"""

import numpy as np

from .map import OSM


class Game:
    osm: OSM
    players: dict[str, "Player"]
    num_players: int
    num_robbers: int
    alerts: list[str]

    def __init__(self):
        self.players = {}
        self.alerts = []

    def num_players_of(self, type: str) -> int:
        return sum(1 for player in self.players.values() if player.type == type)

    def remaining_player_types(self) -> list[str]:
        num_cops = self.num_players_of("cop")
        num_robbers = self.num_players_of("robber")
        remain = []
        for _ in range(self.num_robbers - num_robbers):
            remain.append("robber")
        for _ in range(self.num_players - self.num_robbers - num_cops):
            remain.append("cop")

        return remain


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
