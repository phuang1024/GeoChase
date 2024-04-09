"""
OSM map drawer.
"""

import pygame

from gui.window import ViewWindow
from utils.map import OSM


class MapDrawer:
    def draw(self, view: ViewWindow, osm: OSM) -> pygame.Surface:
        surface = pygame.Surface(view.resolution, pygame.SRCALPHA)

        for way in osm.ways:
            if "addr:street" in way.tags:
                continue

            # Check if in screen bounds.
            """
            left, top = view.coord_to_px(way.top, way.left)
            right, bottom = view.coord_to_px(way.bottom, way.right)
            if right < 0 or left > view.width or top < 0 or bottom > view.height:
                continue
            """

            # Draw lines
            points = view.coord_to_px(way.points)
            pygame.draw.lines(surface, (0, 0, 0, 255), False, points, 1)

        return surface
