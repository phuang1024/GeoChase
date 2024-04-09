"""
Handles scalable, resizable view window of the full OSM.
Wrapper around pygame display.
"""

from dataclasses import dataclass

import numpy as np
import pygame

from constants import *
from utils import *


@dataclass
class ViewWindow:
    """
    Info about conversion between px and coords.
    """
    y_size: float
    """Size of Y display in coords. Coords/screen."""
    pos: np.ndarray
    """Center of display in coords."""
    width: int
    height: int
    stretch_factor: float = 1
    """secant(avg_latitude)"""

    @property
    def resolution(self) -> np.ndarray:
        return np.array([self.width, self.height])

    @property
    def aspect(self) -> float:
        return self.width / self.height

    @property
    def x_size(self) -> float:
        """Coords/screen in x direction."""
        return self.y_size * self.aspect * self.stretch_factor

    @property
    def size(self) -> np.ndarray:
        """Coords/screen in x and y direction."""
        return np.array([self.x_size, self.y_size])

    @property
    def scale(self) -> np.ndarray:
        """px/coord in x and y direction."""
        return self.resolution / self.size

    @property
    def top_left(self) -> np.ndarray:
        """
        Top left corner of window in coords.
        """
        return self.pos - self.size / 2

    def coord_to_px(self, coord: np.ndarray) -> np.ndarray:
        px = (coord - self.top_left) * self.scale
        px[..., 1] = self.height - px[..., 1]
        return px

    def px_to_coord(self, px: np.ndarray) -> np.ndarray:
        px[..., 1] = self.height - px[..., 1]
        return px / self.scale + self.top_left


class Window:
    view_window: ViewWindow

    def __init__(self, osm: OSM):
        self.view_window = ViewWindow(
            0.75 / COORDS_TO_MILES,
            osm.com,
            1280,
            720,
            osm.stretch_factor,
        )

        self.surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

    def update(self, events):
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.view_window.width = event.w
                self.view_window.height = event.h

        self.view_window.pos[0] += 0.0001
        print(self.view_window.pos)
