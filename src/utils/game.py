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

    def __init__(self):
        self.players = {}


class Player:
    id: str
    pos: np.ndarray
    vel: np.ndarray

    def __init__(self, id):
        self.pos = np.zeros(2)
        self.vel = np.zeros(2)
        self.id = id
