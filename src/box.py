from .constants import *
import pygame as pg
from math import floor

pg.init()

Colors = {
    EMPTY: EMPTY_BOX_COLOR,
    SUCCESS: SUCCESS_BOX_COLOR,
    INCORRECT: INCORRECT_BOX_COLOR,
    PARTIAL: PARTIAL_BOX_COLOR
}

letter_font = pg.font.SysFont(FONT, int(BOX_FONT_SIZE), bold=True)


class Box:
    def __init__(self, pos: tuple, size: int, state: int):
        self.pos = pos
        self.size = size
        self.rect = pg.Rect(pos[0], pos[1], size, size)

        self.state = state

        self.box_text = ''

    def set_state(self, state, screen):
        self.state = state
        self.draw(screen)

    def draw(self, screen):
        pg.draw.rect(screen, EMPTY_BOX_COLOR, self.rect, width=0)

        #creating borders for the box
        border_width = floor(self.size*0.05) if self.state == EMPTY else 0

        #coloring the box and font
        font_color = EMPTY_BOX_FONT_COLOR if self.state == EMPTY else TEXT_COLOR
        box_color = Colors.get(self.state)

        # drawing the box and placing the text in the center
        pg.draw.rect(screen, box_color, self.rect, width=border_width)
        text_surface = letter_font.render(self.box_text, True, font_color)
        text_rect = text_surface.get_rect(center = self.rect.center)

        screen.blit(text_surface, text_rect)


if __name__ == '__main__':

    pg.init()
    screen = pg.display.set_mode((800, 600))
    screen.fill((255, 255, 255))
    tb = Box((400, 300), 75, EMPTY)
    pg.display.flip()
    tb.draw(screen)

    # Game Loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        pg.display.update()


