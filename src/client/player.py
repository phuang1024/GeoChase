import numpy as np
import pygame

from constants import *


class Player:
    SIZE = 50
    SPEED = 80 / 1600 / COORDS_TO_MILES

    pos: np.ndarray
    """Center of display in lat, lon coords."""

    def __init__(self, start: np.ndarray, image: str):
        self.pos = np.array(start)

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

    def render(self, surface, map_drawer):
        pixel_pos = map_drawer.project(*self.pos[::-1])
        pixel_pos -= self.SIZE // 2
        surface.blit(self.surface, pixel_pos)
        return surface


class Cop(Player):
    def __init__(self, start: np.ndarray):
        super().__init__(start, "../../assets/cop.png")


class Robber(Player):
    def __init__(self, start: np.ndarray):
        super().__init__(start, "../../assets/robber.png")
