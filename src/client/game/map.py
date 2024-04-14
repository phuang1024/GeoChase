"""
OSM map drawer.
"""

import numpy as np
import pygame

from game.window import ViewWindow
from game.ui import UIStyle
from utils import *


def draw_osm(view: ViewWindow, osm: OSM, ui: UIStyle, width: int = 1) -> pygame.Surface:
    surface = pygame.Surface(view.resolution, pygame.SRCALPHA)

    # View bounds (left, top, right, bottom) in coords.
    view_bounds = view.px_to_coord(np.array([[0, 0], view.resolution])).flatten()

    for way in osm.ways:
        is_building = "addr:street" in way.tags
        is_main_way = way.tags.get("highway", None) in VALID_ROAD_TYPES
        if not ui.draw_buildings and is_building:
            continue

        if is_building or ui.draw_all_ways or is_main_way:
            # Check if in screen bounds.
            if (
                    way.right_bottom[0] < view_bounds[0]
                    or way.left_top[0] > view_bounds[2]
                    or way.right_bottom[1] < view_bounds[3]
                    or way.left_top[1] > view_bounds[1]
                ):
                continue

            # Draw lines
            points = view.coord_to_px(way.nodes)
            pygame.draw.lines(surface, (0, 0, 0, 255), False, points, width if is_main_way else 1)

    return surface
