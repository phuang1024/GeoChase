import numpy as np
import pygame


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
