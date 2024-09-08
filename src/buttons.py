import pygame as pg
from .constants import *

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def get_rect(self):
        return pg.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class DFSButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple, font_size: int):
        super().__init__(x, y, width, height, color)
        self.text = text
        self.font_size = font_size

    def draw(self, screen):
        super().draw(screen)
        font = pg.font.SysFont(FONT, self.font_size)
        text = font.render(self.text, True, TEXT_COLOR)
        screen.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

class BFSButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple, font_size: int):
        super().__init__(x, y, width, height, color)
        self.text = text
        self.font_size = font_size

    def draw(self, screen):
        super().draw(screen)
        font = pg.font.SysFont(FONT, self.font_size)
        text = font.render(self.text, True, TEXT_COLOR)
        screen.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

class BestFSButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple, font_size: int):
        super().__init__(x, y, width, height, color)
        self.text = text
        self.font_size = font_size

    def draw(self, screen):
        super().draw(screen)
        font = pg.font.SysFont(FONT, self.font_size)
        text = font.render(self.text, True, TEXT_COLOR)
        screen.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))


class ClearWindow(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple, font_size: int):
        super().__init__(x, y, width, height, color)
        self.text = text
        self.font_size = font_size

    def draw(self, screen):
        super().draw(screen)
        font = pg.font.SysFont(FONT, self.font_size)
        text = font.render(self.text, True, TEXT_COLOR)
        screen.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))