"""
GUI (pygame) main game loop.
"""

import time

import numpy as np
import pygame

from gui.map import MapDrawer
from gui.sprite import *
from gui.window import Window
from utils import *

SERVER_INTERVAL = 1 / 10


def main(args, game_id, player_id):
    metadata = request(args.host, args.port, {"type": "game_metadata", "game_id": game_id})
    game_state = None
    last_server_update = 0

    surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("GeoChase")
    pygame.display.set_icon(pygame.image.load("../../assets/target.png"))

    osm = metadata["osm"]
    window = Window(osm)
    map_drawer = MapDrawer()
    load_player_sprites()

    player_state = {
        "type": "",
        "pos": metadata["players"][player_id].pos,
        "vel": np.zeros(2),
    }

    while True:
        time.sleep(1 / 60)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return

        if time.time() - last_server_update > SERVER_INTERVAL or game_state is None:
            game_state = request(args.host, args.port, {
                "type": "game_state",
                "game_id": game_id,
                "player_id": player_id,
                "pos": player_state["pos"],
                "vel": player_state["vel"],
            })
            last_server_update = time.time()

            for player in game_state["players"].values():
                if player.id == player_id:
                    player_state["type"] = player.type

        window.update(events)

        surface.fill((255, 255, 255))
        surface.blit(map_drawer.draw(window.view_window, osm), (0, 0))

        draw_sprite(surface, window.view_window, player_state["type"], player_state["pos"])

        pygame.display.update()
