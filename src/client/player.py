import numpy as np
import pygame

from constants import *

SIZE = 50
SPRITES = {
}


def draw_player(surface, map_drawer, type, pos):
    image = SPRITES[type]
    pixel_pos = map_drawer.project(*pos[::-1])
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
    SPRITES["cop"] = load_sprite("../../assets/cop.png")
    #SPRITES["robber"] = load_sprite("../../assets/robber.png")
