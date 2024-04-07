import time

import numpy as np
import pygame

from constants import *
from map_drawer import MapDrawer
from osm import parse_osm_file
from player import Cop, Player, Robber


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
