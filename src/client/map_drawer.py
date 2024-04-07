import numpy as np
import pygame
from utils import *

from constants import *


class MapDrawer:
    osm: OSM
    scale: float
    """Size of Y display in coords."""
    pos: np.ndarray
    """Center of display in lat, lon coords."""

    def __init__(self, osm: OSM):
        self.osm = osm
        self.scale = 0.75 / COORDS_TO_MILES
        self.pos = np.array(self.osm.get_com())

        self.last_surface = None

    def render(self, window) -> pygame.Surface:
        """
        Draws on window in place.

        Returns the shadow of roads (i.e. valid places to drive on).
        """
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill((255, 255, 255, 0))

        road_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        road_surf.fill((255, 255, 255, 0))

        for way in self.osm.ways:
            # Check if in screen bounds.
            left, top = self.project(way.top, way.left)
            right, bottom = self.project(way.bottom, way.right)
            if right < 0 or left > WIDTH or top < 0 or bottom > HEIGHT:
                continue

            points = []
            for node in way.nodes:
                points.append(self.project(node.lat, node.lon))

            if (
                "highway" in way.tags
                and way.tags["highway"].lower().strip() in VALID_ROAD_TYPES
            ):
                pygame.draw.lines(road_surf, (0, 0, 0, 80), False, points, ROAD_WIDTH)
            else:
                pygame.draw.lines(surface, (0, 0, 0, 255), False, points, 1)

        road_surf = pygame.transform.box_blur(road_surf, 2)

        surface.blit(road_surf, (0, 0))

        window.blit(surface, (0, 0))

        self.last_surface = surface

        return surface

    def project(self, lat, lon):
        # Pixels per coord
        y_scale = HEIGHT / self.scale
        x_scale = y_scale / self.osm.stretch_factor
        scale = np.array([x_scale, -y_scale])

        coord_pos = np.array([lon, lat])
        px_pos = (coord_pos - self.pos) * scale + np.array([WIDTH / 2, HEIGHT / 2])

        return px_pos

    def force_road(self, loc, mvt) -> np.ndarray:
        """
        Takes in the current position as well as where the player wants to go
        and returns the new position it can go to while ensuring it stays on
        the road.
        """
        if self.last_surface is None:
            return loc + mvt

        horiz = mvt[0] > mvt[1]
        new_loc = loc + mvt
        pos = self.project(*new_loc[::-1])
        pixels = [pos]

        """
        # check neighboring pixels, removed because causes stuck positions
        if horiz:
            # check vertical pixels
            pixels.append([pos[0], pos[1] + 1])
            pixels.append([pos[0], pos[1] - 1])
        else:
            # check horizontal pixels
            pixels.append([pos[0] + 1, pos[1]])
            pixels.append([pos[0] - 1, pos[1]])
        """

        # check if any of the pixels are not white in order of priority
        for pixel in pixels:
            if self.last_surface.get_at(pixel)[:3] != (255, 255, 255):
                return new_loc

        # none of the pixels were valid, so return the original location
        return loc
