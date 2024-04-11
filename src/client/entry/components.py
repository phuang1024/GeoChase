import pygame

from constants import *


class Button:
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        self.text = text

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return (self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0]
                and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1])

    def is_pressed(self):
        return self.is_hovered() and pygame.mouse.get_pressed()[0]

    def is_clicked(self, events):
        if self.is_pressed():
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False

    def draw(self, surface):
        if self.is_pressed():
            color = 150
        elif self.is_hovered():
            color = 220
        else:
            color = 255

        pygame.draw.rect(surface, (color, color, color), (*self.pos, *self.size))
        pygame.draw.rect(surface, TEXT_COLOR, (*self.pos, *self.size), 2)
        text = FONT_LARGE.render(self.text, True, TEXT_COLOR)
        surface.blit(text, (
            self.pos[0] + (self.size[0] - text.get_width()) / 2,
            self.pos[1] + (self.size[1] - text.get_height()) / 2
        ))
