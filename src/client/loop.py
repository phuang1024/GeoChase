"""
GUI (pygame) main game loop.
"""

import time
from threading import Thread

import numpy as np
import pygame

from collision import *
from constants import *
from mask import *
from map import draw_osm
from sprite import *
from window import Window
from ui import *
from utils import *

FPS = 60
SERVER_INTERVAL = 1 / 10

def _pspeed(type):
    return AIR_SPEED if type == "heli" else GROUND_SPEED


class Clock:
    def __init__(self, fps):
        self.period = 1 / fps
        self.last_tick = 0

    def is_tick(self):
        return time.time() - self.last_tick > self.period

    def tick(self):
        start = time.time()
        while not self.is_tick():
            time.sleep(0.001)
        self.last_tick = time.time()
        return time.time() - start


def server_daemon(args, game_id, player_id, player_state, other_players, is_running, r_game_state):
    """
    is_running: [True] or [False] to stop the daemon
    """
    while is_running[0]:
        time.sleep(SERVER_INTERVAL)

        game_state = request(args.host, args.port, {
            "type": "game_state",
            "game_id": game_id,
            "player_id": player_id,
            "pos": player_state["pos"],
            "vel": player_state["vel"],
        })

        for k, v in game_state.items():
            r_game_state[k] = v
        r_game_state["last_ping"] = time.time()

        for player in game_state["players"].values():
            if player.id == player_id:
                # Initialize player id
                player_state["type"] = player.type
            else:
                # Assume player travels with const vel for half the interval
                other_players["expected"][player.id] = player.pos + player.vel * _pspeed(player.type) * SERVER_INTERVAL / 2


def main(args, game_id, player_id):
    clk_gui = Clock(FPS)

    metadata = request(args.host, args.port, {"type": "game_metadata", "game_id": game_id})
    game_state = {}
    last_loop_time = time.time()

    surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("GeoChase")
    pygame.display.set_icon(pygame.image.load("../../assets/target.png"))

    osm = metadata["osm"]
    ui_style = UIStyle()
    window = Window(osm)
    load_player_sprites()

    coll_surf = None
    player_state = {
        "type": "",
        "pos": metadata["players"][player_id].pos,
        "vel": np.zeros(2),
    }
    # Used to interpolate other players' positions
    other_players = {
        "curr": {},
        "expected": {},
    }

    # Start server daemon
    is_running = [True]
    server_thread = Thread(target=server_daemon, args=(args, game_id, player_id, player_state, other_players, is_running, game_state))
    server_thread.start()
    while not game_state:
        # Wait for first ping
        time.sleep(0.1)

    while is_running[0]:
        idle_time = clk_gui.tick()
        dt = time.time() - last_loop_time
        last_loop_time = time.time()

        # Check global events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                is_running[0] = False
                server_thread.join()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and player_state["type"] == "robber":
                    request(args.host, args.port, {"type": "rob", "game_id": game_id, "pos": player_state["pos"]})

        # Update game state
        player_state["vel"] = get_user_ctrl()
        new_pos = player_state["pos"] + player_state["vel"] * _pspeed(player_state["type"]) * dt

        if player_state["type"] in ("robber", "cop"):
            coll_window, coll_surf = make_coll_info(player_state["pos"], osm)
            if coll_surf.get_at(coll_window.coord_to_px(new_pos).astype(int)).a != 0:
                player_state["pos"] = new_pos
        else:
            player_state["pos"] = new_pos

        ui_style.update(events)
        window.update(events, ui_style, player_state, dt)

        # Draw
        surface.fill((255, 255, 255))

        # Draw map
        surface.blit(draw_osm(window.view_window, osm, ui_style, 2), (0, 0))

        # Draw players
        draw_sprite(surface, window.view_window, player_state["type"], player_state["pos"])
        interp_others(other_players, game_state["last_ping"] + SERVER_INTERVAL - time.time(), dt)
        for player in game_state["players"].values():
            if player.id != player_id:
                draw_sprite(surface, window.view_window, player.type, other_players["curr"][player.id])

        # Draw targets
        if player_state["type"] == "robber":
            for target in game_state["targets"]:
                draw_sprite(surface, window.view_window, "target", target)

        # Draw masks
        if player_state["type"] != "spectator":
            radius = AIR_VIS if player_state["type"] == "heli" else GROUND_VIS
            radius *= window.view_window.scale[1]
            mask = circular_mask(surface.get_size(), window.view_window.coord_to_px(player_state["pos"]), radius)
            surface.blit(mask, (0, 0))

        # Draw UI
        if ui_style.info_style > 0:
            if ui_style.info_style == 2:
                rect = pygame.Surface((270, surface.get_height()), pygame.SRCALPHA)
                rect.fill((255, 255, 255, 220))
                surface.blit(rect, (0, 0))
                surface.blit(rect, (surface.get_width() - 270, 0))

            player_counts = {"robber": 0, "cop": 0, "heli": 0}
            for player in game_state["players"].values():
                if player.type in player_counts:
                    player_counts[player.type] += 1
            game_info = [
                f"pos: {player_state['pos'][0]:.4f} , {player_state['pos'][1]:.4f}",
                f"robbers: {player_counts['robber']}",
                f"cops: {player_counts['cop']}",
                f"helis: {player_counts['heli']}",
            ]
            if player_state["type"] == "robber":
                game_info.append(f"targets: {len(game_state['targets'])}")

            draw_text(surface, TEXT_COLOR, [
                f"fps: {int(1 / dt)}",
                f"res: {surface.get_width()} , {surface.get_height()}",
                f"util: {int(100 * (1 - idle_time / (1 / FPS)))}%",
            ], (20, 20))
            draw_text(surface, (60, 60, 60), game_info, (20, 100))
            draw_text(surface, (60, 60, 60), game_state["alerts"], (surface.get_width() - 250, 20))

        if coll_surf is not None and ui_style.show_coll:
            surface.blit(coll_surf, (0, surface.get_height() - COLL_RES))

        # Update display
        pygame.display.update()
