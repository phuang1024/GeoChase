import math

import numpy as np
import pygame

pygame.init()


WIDTH = 1280
HEIGHT = 720

TEXT_COLOR = (80, 80, 80)

FONT = pygame.font.Font("../../assets/font.ttf", 16)

# earth's circumference / 360
COORDS_TO_MILES = 2 * math.pi * 3959 / 360

ROAD_WIDTH = 15
GROUND_VIS = 0.15 / COORDS_TO_MILES
AIR_VIS = 0.3 / COORDS_TO_MILES
GROUND_SPEED = 80 / 1600 / COORDS_TO_MILES
AIR_SPEED = 130 / 1600 / COORDS_TO_MILES

# Collision calculation
COLL_RES = 100
COLL_RADIUS = 0.04 / COORDS_TO_MILES
COLL_WIDTH = 16
COLL_BLUR = 4
