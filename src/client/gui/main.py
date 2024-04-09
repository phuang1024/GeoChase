"""
GUI (pygame) main game loop.
"""

import time

import pygame

from gui.window import Window


def main(*args):
    window = Window()

    while True:
        time.sleep(1 / 60)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return

        window.update(events)

        pygame.display.update()
