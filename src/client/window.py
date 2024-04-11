"""
Handles scalable, resizable view window of the full OSM.
"""

from dataclasses import dataclass

import numpy as np
import pygame

from constants import *
from ui import UIStyle
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
    DEFAULT_SCALE = 0.3 / COORDS_TO_MILES
    MIN_SCALE = 0.1 / COORDS_TO_MILES
    MAX_SCALE = 3 / COORDS_TO_MILES

    def __init__(self, osm: OSM):
        self.view_window = ViewWindow(
            self.DEFAULT_SCALE,
            osm.center,
            1280,
            720,
            osm.stretch_factor,
        )

        # Used for click and drag.
        self.drag_data = {
            "init_mouse_pos": None,
            "init_window_pos": None,
        }

    def update(self, events, ui_style: UIStyle, player_state, dt):
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.view_window.width = event.w
                self.view_window.height = event.h

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (4, 5):
                    self.view_window.y_size *= (1 / 1.1) if event.button == 4 else 1.1
                    self.view_window.y_size = np.clip(self.view_window.y_size, self.MIN_SCALE, self.MAX_SCALE)

                elif event.button == 1:
                    self.drag_data["init_mouse_pos"] = np.array(event.pos)
                    self.drag_data["init_window_pos"] = self.view_window.pos.copy()

                    ui_style.view_style = 0

        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = np.array(pygame.mouse.get_pos())

        if mouse_pressed[0]:
            if self.drag_data["init_mouse_pos"] is not None:
                delta = (mouse_pos - self.drag_data["init_mouse_pos"]) / self.view_window.scale
                delta[1] *= -1
                self.view_window.pos = self.drag_data["init_window_pos"] - delta

        if ui_style.view_style == 1:
            self.view_window.pos = player_state["pos"].copy()
        elif ui_style.view_style == 2:
            fac = dt * 3
            self.view_window.pos = (1 - fac) * self.view_window.pos + fac * player_state["pos"]
