import math


WIDTH = 1280
HEIGHT = 720

# earth's circumference / 360
COORDS_TO_MILES = 2 * math.pi * 3959 / 360

PLAYER_SPEED = 80 / 1600 / COORDS_TO_MILES

VALID_ROAD_TYPES = (
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "residential",
    "unclassified",
)
