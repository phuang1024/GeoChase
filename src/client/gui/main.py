"""
GUI (pygame) main game loop.
"""

import time

import pygame

from gui.map import MapDrawer
from gui.window import Window
from utils import *


def main(args, game_id, player_id, player_type):
    metadata = request(args.host, args.port, {"type": "game_metadata", "game_id": game_id})

    osm = metadata["osm"]
    window = Window(osm)
    map_drawer = MapDrawer()

    while True:
        time.sleep(1 / 60)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return

        window.update(events)

        window.surface.fill((255, 255, 255))
        window.surface.blit(map_drawer.draw(window.view_window, osm), (0, 0))

        pygame.display.update()
