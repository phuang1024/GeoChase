"""
Draws player sprites.
"""

__all__ = (
    "SPRITES",
    "draw_sprite",
    "load_player_sprites",
    "interp_others",
)

import pygame

from constants import *
from game.map import ViewWindow

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


def interp_others(others, time_left, dt):
    """
    Update `other_players` (in game loop) to get smooth movement of other players.
    Assume that, in `time_left`, player moves from curr to expected.
    Therefore, in this iteration, it moves dt / time_left of the way.
    """
    for id in others["expected"]:
        if id not in others["curr"]:
            others["curr"][id] = others["expected"][id]
        else:
            delta = others["expected"][id] - others["curr"][id]
            others["curr"][id] += delta * dt / time_left
