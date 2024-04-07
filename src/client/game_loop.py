import time

import numpy as np
import pygame
from utils import request

from constants import *
from map_drawer import MapDrawer
from osm import parse_osm_file
from player import *

STATUS_INTERVAL = 0.3


def game_loop(args, game_id, player_id):
    surface = pygame.display.set_mode((WIDTH, HEIGHT))

    osm = parse_osm_file("../../assets/small.osm")
    map_drawer = MapDrawer(osm)

    player_pos = osm.get_com()

    last_time = time.time()
    time_delta = 0
    last_status_time = time.time()

    load_player_sprites()
    other_players = []

    """
    # Store state at mousedown
    click_mouse_pos = None
    click_window_pos = None
    # Updated every iter
    last_mouse_pos = None
    """

    while True:
        time_delta = time.time() - last_time
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                """
                if event.button == 4:
                    map_drawer.scale *= 1.1
                elif event.button == 5:
                    map_drawer.scale /= 1.1
                elif event.button == 1:
                    click_mouse_pos = np.array(event.pos)
                    click_window_pos = map_drawer.pos
                """

        # Handle user movement.
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
            player_pos += player_mvt * PLAYER_SPEED * time_delta

        # Update status with server.
        if time.time() - last_status_time > STATUS_INTERVAL:
            last_status_time = time.time()

            resp = request(args.host, args.port, {
                "type": "game_state",
                "game_id": game_id,
                "player_id": player_id,
                "pos": player_pos,
                "vel": None,
            })
            other_players = resp["players"].values()

        """
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
        """
        map_drawer.pos = player_pos

        # Render
        surface.fill((255, 255, 255))

        map_drawer.render(surface)

        draw_player(surface, map_drawer, "cop", player_pos)
        for player in other_players:
            if player.id == player_id:
                continue
            draw_player(surface, map_drawer, "cop", player.pos)

        pygame.display.update()
