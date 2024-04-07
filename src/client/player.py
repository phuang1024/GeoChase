import math

import numpy as np
import pygame
from osm import OSM, parse_osm_file

WIDTH = 1280
HEIGHT = 720

COORDS_TO_MILES = 2 * math.pi * 3959 / 360


class Player:
    SIZE = 50
    SPEED = 1

    pos: np.ndarray
    """Center of display in lat, lon coords."""

    def __init__(self, start: np.ndarray, image: str):
        self.pos = start

        img = pygame.image.load(image).convert_alpha()
        img_surf = pygame.transform.scale(img, (self.SIZE, self.SIZE))
        self.surface = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(img_surf, (0, 0))
        pygame.draw.circle(
            self.surface,
            (255, 0, 0),
            (self.SIZE // 2, self.SIZE // 2),
            self.SIZE // 2,
            2,
        )

    def render(self, surface):
        surface.blit(self.surface, self.pos)
        return surface

    def move_up(self):
        self.pos[1] -= self.SPEED

    def move_down(self):
        self.pos[1] += self.SPEED

    def move_left(self):
        self.pos[0] -= self.SPEED

    def move_right(self):
        self.pos[0] += self.SPEED


class Cop(Player):
    def __init__(self, start: np.ndarray):
        super().__init__(start, "../../assets/cop.png")


class Robber(Player):
    def __init__(self, start: np.ndarray):
        super().__init__(start, "../../assets/robber.png")
