import pygame as pg
import os
from .constants import *
from .game import Game


def main():
    pg.init()

    # Screen
    screen = pg.display.set_mode((int(WIDTH), int(HEIGHT)))
    pg.display.set_caption(TITLE)
    screen.fill(BG_COLOR)
    pg.display.flip()

    # Main Game
    words_list = open(WORDS_LIST).read()
    words_list = words_list.split('\n')
    game = Game(screen, WORD_LENGTH, words_list)

    # Game Loop
    running = True
    while running:
        for event in pg.event.get():

            # # Key Pressed
            if not game.game_state.finished:
                if event.type == pg.KEYDOWN and 97 <= event.key <= 122:         # a-z
                    game.write_letter(chr(event.key))

                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:    # Backspace
                    game.delete_letter()

                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:       # Enter
                    game.enter_word()

            # Quitting the game
            if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                running = False
    
        pg.display.update()