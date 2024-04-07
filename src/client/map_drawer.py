import numpy as np
import pygame
from constants import *

from utils import *


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

        self.roads_pos = self.pos.copy()
        self.roads_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self.last_surface = None

    def render(self, window, road_width=ROAD_WIDTH) -> pygame.Surface:
        """
        Draws on window in place.

        Returns the shadow of roads (i.e. valid places to drive on).
        """
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill((255, 255, 255, 0))

        road_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        road_surf.fill((255, 255, 255, 0))

        for way in self.osm.ways:
            if "addr:street" in way.tags:
                continue

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
                pygame.draw.lines(road_surf, (0, 0, 0, 80), False, points, road_width)
            else:
                pygame.draw.lines(surface, (0, 0, 0, 255), False, points, 1)

        road_surf = pygame.transform.box_blur(road_surf, 2)
        surface.blit(road_surf, (0, 0))

        roads_pos = self.project(*self.roads_pos[::-1])
        surface.blit(self.roads_surf, roads_pos - np.array([WIDTH / 2, HEIGHT / 2]))

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

    def update_roads(self):
        font = pygame.font.SysFont("Arial", ROAD_WIDTH, True)

        self.roads_surf.fill((255, 255, 255, 0))

        self.roads_pos = self.pos.copy()

        for way in self.osm.ways:
            if "addr:street" not in way.tags:
                continue

            if np.random.rand() < STREET_NAME_CHANCE:
                text = font.render(way.tags["addr:street"], True, (0, 0, 0, 120))
                n1 = way.nodes[0]
                # n2 = way.nodes[min(int(text.get_width() / 25), len(way.nodes) - 1)]
                n2 = way.nodes[1]
                node1 = self.project(n1.lat, n1.lon)
                node2 = self.project(n2.lat, n2.lon)
                angle = np.degrees(np.arctan2(node2[1] - node1[1], node2[0] - node1[0]))
                if angle < -90:
                    angle = -(angle + 270)
                else:
                    angle = 90 - angle

                if abs(angle) > 90:
                    angle += 180
                text = pygame.transform.rotate(text, angle)
                node1 -= np.array([text.get_width() / 2, text.get_height() / 2])
                self.roads_surf.blit(text, node1)

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
