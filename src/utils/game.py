"""
Classes relating to gameplay.
"""

from dataclasses import dataclass

from .map import Map


@dataclass
class GameConfig:
    pass


class Game:
    config: GameConfig
    map: Map
