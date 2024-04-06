import math

import numpy as np
import pygame

from osm import OSM, parse_osm_file

WIDTH = 1280
HEIGHT = 720

COORDS_TO_MILES = 2 * math.pi * 3959 / 360


class MapDrawer:
    osm: OSM
    scale: float
    """Size of Y display in coords."""
    pos: np.ndarray
    """Topleft of display in lat, lon coords."""

    def __init__(self, osm: OSM):
        self.osm = osm
        self.scale = 1 / COORDS_TO_MILES
        self.pos = np.array(self.osm.get_com())

    def render(self, surface):
        print("Render")
        surface.fill((255, 255, 255))

        get_px = lambda node: self.project(node.lat, node.lon)
        in_bounds = lambda px: 0 <= px[0] <= WIDTH and 0 <= px[1] <= HEIGHT

        for way in self.osm.ways:
            for i in range(len(way.nodes) - 1):
                p1 = get_px(way.nodes[i])
                p2 = get_px(way.nodes[i + 1])
                if in_bounds(p1) or in_bounds(p2):
                    pygame.draw.line(surface, (0, 0, 0), p1, p2, 1)

        return surface

    def project(self, lat, lon):
        # Pixels per coord
        y_scale = HEIGHT / self.scale
        x_scale = y_scale / self.osm.stretch_factor
        scale = np.array([x_scale, -y_scale])

        coord_pos = np.array([lon, lat])
        px_pos = (coord_pos - self.pos) * scale

        return px_pos


def game_loop():
    surface = pygame.display.set_mode((WIDTH, HEIGHT))

    osm = parse_osm_file("../../assets/test.osm")
    map_drawer = MapDrawer(osm)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        map_drawer.render(surface)
        pygame.display.flip()
