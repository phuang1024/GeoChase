import time

import numpy as np
import pygame
from utils import *

from constants import *
from map_drawer import MapDrawer
from player import *

STATUS_INTERVAL = 0.15


def get_mvt_input():
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
    else:
        player_mvt = np.array([0, 0])

    return player_mvt


def draw_info(surface, x, texts):
    for i, text in enumerate(texts):
        text_surf = FONT.render(text, True, (80, 80, 80))
        surface.blit(text_surf, (x, i * 18 + 35))


def game_loop(args, game_id, player_id, player_type):
    surface = pygame.display.set_mode((WIDTH, HEIGHT))

    metadata = request(args.host, args.port, {"type": "game_metadata", "game_id": game_id})
    osm = metadata["osm"]
    map_drawer = MapDrawer(osm)
    map_drawer.update_roads()
    if player_type == "heli":
        map_drawer.scale *= 1.3

    player_pos = np.array(osm.get_rand_pos())
    last_player_pos = player_pos.copy()

    last_time = time.time()
    time_delta = 0
    last_status_time = time.time()
    status = None

    load_player_sprites()

    while True:
        time.sleep(0.01)

        time_delta = time.time() - last_time
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and player_type == "robber":
                    request(args.host, args.port, {"type": "rob", "game_id": game_id, "pos": player_pos})

        # Handle user movement.
        player_mvt = get_mvt_input()
        if player_type == "heli":
            player_pos += player_mvt * PLAYER_SPEED * time_delta * 2
        else:
            player_pos = map_drawer.force_road(player_pos, player_mvt * PLAYER_SPEED * time_delta)
        map_drawer.pos = player_pos

        # Update status with server.
        if status is None or time.time() - last_status_time > STATUS_INTERVAL:
            status = request(args.host, args.port, {
                "type": "game_state",
                "game_id": game_id,
                "player_id": player_id,
                "pos": player_pos,
                "vel": player_mvt,
            })
            last_status_time = time.time()

        # Render
        surface.fill((255, 255, 255))
        map_drawer.render(surface)
        draw_player(surface, map_drawer, player_type, player_pos)

        # Draw other players
        update_elapse = time.time() - last_status_time
        for player in status["players"].values():
            if player.id == player_id:
                continue

            pos = player.pos + player.vel * PLAYER_SPEED * update_elapse
            draw_player(surface, map_drawer, player.type, pos)

        # Update roads
        if np.linalg.norm(player_pos - last_player_pos) > 0.0065:
            map_drawer.update_roads()
            last_player_pos = player_pos.copy()

        # Draw targets
        if player_type == "robber":
            for target in status["targets"]:
                draw_player(surface, map_drawer, "target", target)

        # Visibility mask
        if player_type != "heli":
            surface.blit(VISIBILITY_MASK, (0, 0))

        # Info
        draw_info(surface, 30, [
            f"Num players: {metadata['num_players']}",
            f"Num robbers: {metadata['num_robbers']}",
            f"Remaining targets: {len(status['targets'])}",
            f"Position: {player_pos[0]:.4f}, {player_pos[1]:.4f}",
            f"Velocity: {player_mvt[0]:.1f}, {player_mvt[1]:.1f}",
        ])
        draw_info(surface, WIDTH - 300, status["alerts"])

        pygame.display.update()
