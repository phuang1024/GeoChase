import numpy as np
import pygame

from constants import *
from osm import OSM


class MapDrawer:
    osm: OSM
    scale: float
    """Size of Y display in coords."""
    pos: np.ndarray
    """Center of display in lat, lon coords."""

    def __init__(self, osm: OSM):
        self.osm = osm
        self.scale = 1 / COORDS_TO_MILES
        self.pos = np.array(self.osm.get_com())

    def render(self, surface):
        surface.fill((255, 255, 255))

        for way in self.osm.ways:
            # Check if in screen bounds.
            left, top = self.project(way.top, way.left)
            right, bottom = self.project(way.bottom, way.right)
            if right < 0 or left > WIDTH or top < 0 or bottom > HEIGHT:
                continue

            points = []
            for node in way.nodes:
                points.append(self.project(node.lat, node.lon))
            pygame.draw.lines(surface, (0, 0, 0), False, points, 5)

        return surface

    def project(self, lat, lon):
        # Pixels per coord
        y_scale = HEIGHT / self.scale
        x_scale = y_scale / self.osm.stretch_factor
        scale = np.array([x_scale, -y_scale])

        coord_pos = np.array([lon, lat])
        px_pos = (coord_pos - self.pos) * scale + np.array([WIDTH / 2, HEIGHT / 2])

        return px_pos
