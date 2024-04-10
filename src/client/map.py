"""
OSM map drawer.
"""

import numpy as np
import pygame

from window import ViewWindow
from utils import *


class MapDrawer:
    def draw(self, view: ViewWindow, osm: OSM) -> pygame.Surface:
        surface = pygame.Surface(view.resolution, pygame.SRCALPHA)

        # View bounds (left, top, right, bottom) in coords.
        view_bounds = view.px_to_coord(np.array([[0, 0], view.resolution])).flatten()

        for way in osm.ways:
            # Don't draw buildings.
            if "addr:street" in way.tags:
                continue

            # Check if in screen bounds.
            if (
                    way.right_bottom[0] < view_bounds[0]
                    or way.left_top[0] > view_bounds[2]
                    or way.right_bottom[1] < view_bounds[3]
                    or way.left_top[1] > view_bounds[1]
                ):
                continue

            if way.tags.get("highway", None) not in VALID_ROAD_TYPES:
                continue

            # Draw lines
            points = view.coord_to_px(way.nodes)
            pygame.draw.lines(surface, (0, 0, 0, 255), False, points, 1)

        return surface
