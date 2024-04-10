from dataclasses import dataclass

import numpy as np
import pygame


@dataclass
class UIStyle:
    view_style: str = "follow"
    """'follow' or 'free'."""

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    self.view_style = "follow" if self.view_style == "free" else "free"


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
