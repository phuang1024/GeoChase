import numpy as np
import pygame


class Display:

    WIDTH = 1280
    HEIGHT = 720

    def __init__(self, data):
        self.data = data

    def render(self):
        surface = pygame.Surface((800, 600))
        surface.fill((255, 255, 255))

        for way in self.data.ways:
            for i in range(len(way.nodes) - 1):
                p1 = self.project(way.nodes[i].lat, way.nodes[i].lon)
                p2 = self.project(
                    way.nodes[i + 1].lat, way.nodes[i + 1].lon
                )
                pygame.draw.line(surface, (0, 0, 0), p1, p2, 1)

        return surface

    def project(self, lat, lon):
        x_size = self.WIDTH
        y_size = (
            self.data.scaling_factor
            * x_size
            * (self.data.top - self.data.bottom)
            / (self.data.right - self.data.left)
        )
        x = np.interp(lon, [self.data.left, self.data.right], [-x_size / 2, x_size / 2])
        y = -np.interp(lat, [self.data.top, self.data.bottom], [y_size / 2, -y_size / 2])
        x += self.WIDTH / 2
        y += self.WIDTH / 2
        return x, y
