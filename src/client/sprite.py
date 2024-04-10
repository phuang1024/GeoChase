"""
Draws player sprites.
"""

__all__ = (
    "SPRITES",
    "draw_sprite",
    "load_player_sprites",
)

import pygame

from constants import *
from map import ViewWindow

SIZE = 50
SPRITES = {}


def draw_sprite(surface, view_window: ViewWindow, type, pos):
    if type == "spectator":
        return

    image = SPRITES[type]
    pixel_pos = view_window.coord_to_px(pos)
    pixel_pos -= SIZE // 2
    surface.blit(image, pixel_pos)


def load_sprite(image: str):
    img = pygame.image.load(image).convert_alpha()
    img_surf = pygame.transform.scale(img, (SIZE, SIZE))

    surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    surface.blit(img_surf, (0, 0))
    pygame.draw.circle(
        surface,
        (255, 0, 0),
        (SIZE // 2, SIZE // 2),
        SIZE // 2,
        2,
    )

    return surface


def load_player_sprites():
    for name in ("cop", "robber", "heli", "target"):
        SPRITES[name] = load_sprite(f"../../assets/{name}.png")
