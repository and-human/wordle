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
        """
        Set the state of the box
        """
        self.state = state
        self.draw(screen)

    def set_text(self, text, screen):
        """
        Set the letter in the box
        """
        self.box_text = text
        self.draw(screen)

    def get_text(self):
        """
        Get the letter in the box
        """
        return self.box_text

    def delete_text(self, screen):
        """
        Delete the letter in the box
        """
        self.box_text = ''
        self.draw(screen)

    def draw(self, screen):
        """
        Draw the box on the screen
        """
        # Creating the empty box by deleting if anything before
        pg.draw.rect(screen, EMPTY_BOX_COLOR, self.rect, width=0)

        # Creating borders for the box
        border_width = floor(self.size*0.05) if self.state == EMPTY else 0

        # Coloring the box and font
        font_color = EMPTY_BOX_FONT_COLOR if self.state == EMPTY else TEXT_COLOR
        box_color = Colors.get(self.state)

        # Drawing the box and placing the text in the center
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


