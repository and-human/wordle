import pygame as pg
import os
from .constants import *
from .game import Game
from .buttons import *


def main():
    pg.init()

    # Screen
    screen = pg.display.set_mode((int(WIDTH), int(HEIGHT)))
    pg.display.set_caption(TITLE)
    screen.fill(BG_COLOR)
    pg.display.flip()

    # Game name on top of the window
    font = pg.font.Font(GAME_FONT, 200)
    text = font.render(GAME_TITLE, True, SUCCESS_BG_COLOR)
    screen.blit(text, (WIDTH * 0.31, HEIGHT * 0.05))

    # Clear Grid Button
    clear_button = ClearWindow(int(WIDTH * 0.8), int(HEIGHT * 0.3), BUTTON_WIDTH, BUTTON_HEIGHT, "Clear Grid", BUTTON_COLOR, 24)

    # DFS Solver Button
    dfs_button = DFSButton(int(WIDTH * 0.8), int(HEIGHT * 0.5), BUTTON_WIDTH, BUTTON_HEIGHT, "DFS Solver", BUTTON_COLOR, 24)

    # Main Game
    words_list = open(WORDS_LIST).read()
    words_list = words_list.split('\n')
    words_list = [word.upper() for word in words_list]
    game = Game(screen, WORD_LENGTH, words_list)

    # Game Loop
    running = True
    pg.event.clear()

    while running:

        clear_button.draw(screen)
        dfs_button.draw(screen)

        for event in pg.event.get():

            # Key Pressed
            if not game.game_state.finished:

                #TODO: Block key presses that have already been guessed
                #TODO: Cannot type after using DFS Solver

                if event.type == pg.KEYDOWN and 97 <= event.key <= 122:         # a-z
                    game.write_letter(chr(event.key))

                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:    # Backspace
                    game.delete_letter()

                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:       # Enter
                    game.enter_word()

            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()

                if dfs_button.get_rect().collidepoint(pos):
                    game.solve("DFS")

                if clear_button.get_rect().collidepoint(pos):
                    game.clear()

            # Quitting the game
            if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                running = False
    
        pg.display.update()