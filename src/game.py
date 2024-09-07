import random
import pygame as pg
import os
from .constants import *
from .updatesWindow import UpdatesWindow
from .box import Box
from .gameStates import *
from .searchMethods import *

# Map letters to colors
letter_states = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0,
    'E': 0,
    'F': 0,
    'G': 0,
    'H': 0,
    'I': 0,
    'J': 0,
    'K': 0,
    'L': 0,
    'M': 0,
    'N': 0,
    'O': 0,
    'P': 0,
    'Q': 0,
    'R': 0,
    'S': 0,
    'T': 0,
    'U': 0,
    'V': 0,
    'W': 0,
    'X': 0,
    'Y': 0,
    'Z': 0
}

class Game:
    def __init__(self, screen, word_length: int, word_list: list):
        self.screen = screen
        self.word_length = word_length
        self.word_list = word_list
        self.game_state = PlayState()

        self.game_matrix = []
        self.target_word = (word_list[random.randint(0, len(word_list) - 1)]).upper()

        print(self.target_word)

        # Counter variables for keeping track of letters entered
        self.current_line   = 0
        self.current_letter = 0

        # Creating the text boxes for the game
        self._create_text_boxes()

    def write_letter(self, letter: str):
        """
        Write the letter in the box
        """
        if self.current_letter < self.word_length:
            letter = letter.upper()
            self.game_matrix[self.current_line][self.current_letter].set_text(letter, self.screen)
            self.current_letter += 1

    def delete_letter(self):
        """
        Delete the letter in the box
        """
        if self.current_letter > 0:
            self.current_letter -= 1
            self.game_matrix[self.current_line][self.current_letter].delete_text(self.screen)

    def get_state(self):
        """
        Return the current state of the game
        """
        return self.game_state
    
    def set_state(self, state):
        """
        Set the state of the game
        """
        self.game_state = state

    def enter_word(self):
        """
        Enter the word in the box
        """
        if self.current_letter == self.word_length:
            word_result = self._validate_word()

            # Checking the result of the word
            if word_result == SUCCESS:
                print(letter_states)
                self.game_state = WinState()

            elif word_result == NOT_FOUND:
                self.game_state = WordNotFound()

            elif self.current_line == ATTEMPTS - 1:
                self.game_state = LoseState()

            else:
                self.game_state = PlayState()
                self.current_line += 1
                self.current_letter = 0

    def solve(self, method: str):
        """
        Solve the game using the specified method
        """
        if method == 'DFS':
            dfs = DFS(self)
            dfs.solve()

    def clear(self):
        """
        Clear the game
        """
        self.game_matrix = []
        self.target_word = (self.word_list[random.randint(0, len(self.word_list) - 1)]).upper()

        # Counter variables for keeping track of letters entered
        self.current_line   = 0
        self.current_letter = 0

        # Creating the text boxes for the game
        self._create_text_boxes()


    def _create_text_boxes(self):
        """
        Create the text boxes for the game
        """
        for i in range(int(ATTEMPTS)):
            row = []

            # Creating boxes for each letter in a row
            for j in range(self.word_length):
                pos = (WIDTH * 0.40) + ROW_GUTTER + (j * ROW_GUTTER + j * BOX_SIZE), (HEIGHT * 0.1) + (i * ROW_GUTTER + i * BOX_SIZE)

                # Creating an empty box for the letter
                unit_box = Box(pos, BOX_SIZE, 0)
                unit_box.draw(self.screen)
                row.append(unit_box)

            self.game_matrix.append(row)

        #TODO: Create the keyboard view

        #TODO: Add the button for DFS Solver

        #TODO: Add the button for resetting the game

        pos = (WIDTH * 0.1, HEIGHT * 0.1)
        window = UpdatesWindow(pos, WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, self.game_state.text) 

        window.draw(self.screen)
    
    def _validate_word(self):
        """
        Validate the word entered by the user
        """
        word = ''
        for i in range(self.word_length):
            word += self.game_matrix[self.current_line][i].get_text()

        if word not in self.word_list:
            return NOT_FOUND
        
        # Update the state of boxes
        for i in range(self.word_length):
            letter = self.game_matrix[self.current_line][i].get_text()

            if letter == self.target_word[i]:
                box_state = SUCCESS
                letter_states[letter] = 3
            elif letter in self.target_word:
                box_state = PARTIAL
                letter_states[letter] = 2
            else:
                box_state = INCORRECT
                letter_states[letter] = 1

            self.game_matrix[self.current_line][i].set_state(box_state, self.screen)

        return SUCCESS if word == self.target_word else INCORRECT

            

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    game = Game(screen, WORD_LENGTH, ['hello', 'world', 'python'])
    pg.display.update()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        pg.display.update()