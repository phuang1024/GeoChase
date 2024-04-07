import math

import numpy as np
import pygame

pygame.init()


WIDTH = 1280
HEIGHT = 720

FONT = pygame.font.SysFont("courier", 16)

# earth's circumference / 360
COORDS_TO_MILES = 2 * math.pi * 3959 / 360

ROAD_WIDTH = 15
VISIBILITY = 350

STREET_NAME_CHANCE = .2

PLAYER_SPEED = 120 / 1600 / COORDS_TO_MILES

VISIBILITY_MASK = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
VISIBILITY_MASK.fill((255, 255, 255, 255))
for i in range(VISIBILITY, 0, -1):
    opacity = np.interp(i, [0.8, VISIBILITY], [0, 255])
    opacity = min(max(int(opacity), 0), 255)
    pygame.draw.circle(VISIBILITY_MASK, (255, 255, 255, opacity), (WIDTH // 2, HEIGHT // 2), i)
