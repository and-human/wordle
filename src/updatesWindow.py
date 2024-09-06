import pygame as pg
import os

from .constants import *

pg.init()

letter_font = pg.font.SysFont(FONT, int(WINDOW_FONT_SIZE), bold=True)

class UpdatesWindow:

    def __init__(self, pos: tuple, window_width: int, window_height: int, color, text: str = ''):
        self.pos = pos
        self.window_width = window_width
        self.window_height = window_height
        self.text = text
        self.color = color
        self.rect = pg.Rect(pos[0], pos[1], window_width, window_height)

    def set_text(self, text, screen):
        """
        Set the text in the box
        """
        self.letter = text
        self.draw(screen)

    def set_colour(self, color):
        """
        Set the color of the text in the box
        """
        self.color = color
        self.draw(screen)

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.color, self.rect, width=0)

        # Customise text, create a font surface and blit it to the screen
        text_color = TEXT_COLOR if self.color else EMPTY_BOX_COLOR
        text_surface = letter_font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center = self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, subject):
        game_state = subject.get_state()
        self.set_text(game_state.text, game_state.screen)



if __name__ == '__main__':
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    updates_window = UpdatesWindow((WIDTH * .75, HEIGHT * 0.05), WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR)
    updates_window.set_text('WORDLE', screen)
    pg.display.update()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.display.update()