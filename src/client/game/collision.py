"""
Calculate collisions with edge of road,
and keep player within roads.
"""

import pygame

from constants import *
from game.map import *
from game.window import ViewWindow
from game.ui import UIStyle

COLL_STYLE = UIStyle(
    view_style=True,
    info_style=0,
    draw_buildings=False,
    draw_all_ways=False,
)


def make_coll_info(pos, osm: OSM) -> tuple[ViewWindow, pygame.Surface]:
    window = ViewWindow(
        y_size=COLL_RADIUS * 2,
        pos=pos,
        width=COLL_RES,
        height=COLL_RES,
        stretch_factor=osm.stretch_factor,
    )
    surface = draw_osm(window, osm, UIStyle(), width=COLL_WIDTH)
    surface = pygame.transform.box_blur(surface, COLL_BLUR)
    return window, surface
