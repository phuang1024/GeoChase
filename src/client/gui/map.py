"""
OSM map drawer.
"""

import numpy as np
import pygame

from gui.window import ViewWindow
from utils.map import OSM


class MapDrawer:
    def draw(self, view: ViewWindow, osm: OSM) -> pygame.Surface:
        surface = pygame.Surface(view.resolution, pygame.SRCALPHA)

        # View bounds (left, top, right, bottom) in coords.
        view_bounds = view.px_to_coord(np.array([[0, 0], view.resolution])).flatten()

        for way in osm.ways:
            if "addr:street" in way.tags:
                continue

            # Check if in screen bounds.
            if way.right < view_bounds[0] or way.left > view_bounds[2] or way.top < view_bounds[3] or way.bottom > view_bounds[1]:
                continue

            # Draw lines
            points = view.coord_to_px(way.points)
            pygame.draw.lines(surface, (0, 0, 0, 255), False, points, 1)

        return surface
