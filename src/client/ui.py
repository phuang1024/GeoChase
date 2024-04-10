from dataclasses import dataclass

import numpy as np
import pygame

from constants import *


@dataclass
class UIStyle:
    view_style: bool = True
    """True is follow, False is free"""
    info_style: int = 2
    """0=no, 1=text, 2=text+bg"""
    draw_buildings: bool = False
    draw_all_ways: bool = False

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    self.view_style = not self.view_style
                elif event.key == pygame.K_i:
                    self.info_style = (self.info_style + 1) % 3
                elif event.key == pygame.K_b:
                    self.draw_buildings = not self.draw_buildings
                elif event.key == pygame.K_p:
                    self.draw_all_ways = not self.draw_all_ways


def get_user_ctrl():
    """
    Return velocity based on keyboard input.
    abs(vel) = 1.
    """
    key_pressed = pygame.key.get_pressed()
    vel = np.zeros(2)

    if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
        vel[1] += 1
    if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
        vel[1] -= 1
    if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
        vel[0] -= 1
    if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
        vel[0] += 1

    if np.any(vel):
        vel /= np.linalg.norm(vel)

    return vel


def draw_text(surface, color, lines, pos):
    for i, line in enumerate(lines):
        text = FONT.render(line, True, color)
        surface.blit(text, (pos[0], pos[1] + i * 20))
