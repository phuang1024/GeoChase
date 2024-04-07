__all__ = (
    "GameConfig",
    "Game",
    "Player",
)

"""
Classes relating to gameplay.
"""

from dataclasses import dataclass

import numpy as np

from .map import OSM


@dataclass
class GameConfig:
    num_players: int
    num_robbers: int
    osm: OSM


class Game:
    config: GameConfig
    players: dict[str, "Player"]
    num_players: int

    def __init__(self, num_players):
        self.players = {}
        self.num_players = num_players


class Player:
    id: str
    pos: np.ndarray
    vel: np.ndarray

    def __init__(self, id):
        self.pos = np.zeros(2)
        self.vel = np.zeros(2)
        self.id = id
