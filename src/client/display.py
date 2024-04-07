import math
import time

import numpy as np
import pygame
from osm import OSM, parse_osm_file
from player import Cop, Player, Robber

from utils import COORDS_TO_MILES

WIDTH = 1280
HEIGHT = 720


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


def game_loop():
    surface = pygame.display.set_mode((WIDTH, HEIGHT))

    osm = parse_osm_file("/tmp/big.osm")
    map_drawer = MapDrawer(osm)

    player = Cop(osm.get_com())

    last_time = time.time()
    time_delta = 0

    # Store state at mousedown
    click_mouse_pos = None
    click_window_pos = None
    # Updated every iter
    last_mouse_pos = None

    while True:
        time_delta = time.time() - last_time
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    map_drawer.scale *= 1.1
                elif event.button == 5:
                    map_drawer.scale /= 1.1
                elif event.button == 1:
                    click_mouse_pos = np.array(event.pos)
                    click_window_pos = map_drawer.pos

        keys = pygame.key.get_pressed()
        player_mvt = np.array([0, 0])
        if keys[pygame.K_UP]:
            player_mvt[1] += 1
        if keys[pygame.K_DOWN]:
            player_mvt[1] -= 1
        if keys[pygame.K_LEFT]:
            player_mvt[0] -= 1
        if keys[pygame.K_RIGHT]:
            player_mvt[0] += 1
        if player_mvt.any():
            player_mvt = player_mvt / np.linalg.norm(player_mvt)
            player.pos += player_mvt * player.SPEED * time_delta

        # Handle mouse drag
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = np.array(pygame.mouse.get_pos())
        if mouse_pressed[0] and (mouse_pos != last_mouse_pos).any():
            mouse_delta = mouse_pos - click_mouse_pos

            # Pixels per coord
            y_scale = HEIGHT / map_drawer.scale
            x_scale = y_scale / map_drawer.osm.stretch_factor
            scale = np.array([x_scale, -y_scale])

            map_drawer.pos = click_window_pos - mouse_delta / scale

        map_drawer.render(surface)
        player.render(surface, map_drawer)
        pygame.display.update()