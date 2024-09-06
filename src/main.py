import pygame as pg
import os
from .constants import *
from .game import Game


def main():
    pg.init()

    # Screen
    screen = pg.display.set_mode((int(os.getenv('WIDTH')), int(os.getenv('HEIGHT'))))
    pg.display.set_caption(os.getenv('TITLE'))
    screen.fill(tuple(map(int, os.getenv('BG_COLOR').split(','))))
    pg.display.flip()

    # Main Game
    words_list = ['']
    game = Game(screen, WORD_LENGTH, words_list)

    # Game Loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    
        pg.display.update()