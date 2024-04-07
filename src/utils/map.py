__all__ = (
    "Map",
    "COORDS_TO_MILES",
)

"""
Classes relating to map data.
"""

import math

# earth's circumference / 360
COORDS_TO_MILES = 2 * math.pi * 3959 / 360


class Map:
    pass
