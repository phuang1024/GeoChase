"""
Calculate collisions with edge of road,
and keep player within roads.
"""

import pygame

from constants import *
from map import *
from window import ViewWindow
from ui import UIStyle

COLL_STYLE = UIStyle(
    view_style=True,
    info_style=0,
    draw_buildings=False,
    draw_all_ways=False,
)


def make_roads_surf(pos, osm: OSM):
    window = ViewWindow(
        y_size=COLL_RADIUS * 2,
        pos=pos,
        width=COLL_RES,
        height=COLL_RES,
        stretch_factor=osm.stretch_factor,
    )
    surface = draw_osm(window, osm, UIStyle(), width=COLL_WIDTH)
    surface = pygame.transform.box_blur(surface, COLL_BLUR)
    return surface
