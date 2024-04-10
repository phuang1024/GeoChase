"""
Handle visibility masks.
"""

import pygame


def circular_mask(res, center, radius, blur=20) -> pygame.Surface:
    mask = pygame.Surface(res, pygame.SRCALPHA)
    mask.fill((255, 255, 255, 255))
    pygame.draw.circle(mask, (255, 255, 255, 0), center, radius)
    for i in range(blur):
        pygame.draw.circle(mask, (255, 255, 255, i * 255 // blur), center, radius + i, 2)

    return mask
