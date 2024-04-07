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

from .map import Map


@dataclass
class GameConfig:
    pass


class Game:
    config: GameConfig
    map: Map
    players: dict[str, "Player"]
    num_players: int

    def __init__(self, num_players):
        self.players = {}
        self.num_players = num_players


class Player:
    pos: np.ndarray
    vel: np.ndarray

    def __init__(self):
        self.pos = np.zeros(2)
        self.vel = np.zeros(2)
