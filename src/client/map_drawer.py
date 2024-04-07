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

    def render(self, window) -> pygame.Surface:
        """
        Draws on window in place.

        Returns the shadow of roads (i.e. valid places to drive on).
        """
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        for way in self.osm.ways:
            # Check if in screen bounds.
            left, top = self.project(way.top, way.left)
            right, bottom = self.project(way.bottom, way.right)
            if right < 0 or left > WIDTH or top < 0 or bottom > HEIGHT:
                continue

            points = []
            for node in way.nodes:
                points.append(self.project(node.lat, node.lon))

            if "highway" in way.tags and way.tags["highway"].lower().strip() in VALID_ROAD_TYPES:
                pygame.draw.lines(surface, (0, 0, 0, 80), False, points, 10)
            else:
                pygame.draw.lines(surface, (0, 0, 0, 255), False, points, 1)

        window.blit(surface, (0, 0))

        return surface

    def project(self, lat, lon):
        # Pixels per coord
        y_scale = HEIGHT / self.scale
        x_scale = y_scale / self.osm.stretch_factor
        scale = np.array([x_scale, -y_scale])

        coord_pos = np.array([lon, lat])
        px_pos = (coord_pos - self.pos) * scale + np.array([WIDTH / 2, HEIGHT / 2])

        return px_pos
