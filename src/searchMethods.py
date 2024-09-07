from .constants import *
import pygame as pg
from .gameStates import *
from .game import Game

class DFS:
    def __init__(self, game):
        self.game = game
        self.visited = set()   # Track guessed words to avoid repeating guesses
        self.solution_found = False
        self.correct_positions = [''] * game.word_length  # Correct letters in the exact positions
        self.partial_letters = set()  # Letters that are in the word but not in the correct positions
        self.incorrect_letters = set()  # Letters that are not in the word
        self.num_guesses = 0 # Number of guesses made so far

    def solve(self):
        """
        Initiates the DFS search to solve the game.
        """
        print("Starting DFS search...")
        self._dfs_search([])

    def _dfs_search(self, path):
        """
        Recursively performs a DFS search to find the target word using feedback.
        """
        if self.solution_found:
            return

        # Save the current state for backtracking
        saved_state = self._save_game_state()

        # Filter the word list based on known constraints
        filtered_words = self._filter_words()

        # Iterate over all possible words in the filtered list
        for word in filtered_words:
            if self.solution_found:
                break  

            #TODO: The last row gets filled with the colors but not the letters
            if self.num_guesses > ATTEMPTS:
                print("Exceeded maximum number of guesses.", self.num_guesses)
                self.solution_found = True
                break

            if word not in self.visited:
                self.visited.add(word)
                print(f"Trying word: {word}")
                self.num_guesses += 1

                # Simulate making the guess
                self._make_guess(word)

                # Process feedback from the guess
                self._process_feedback(word)

                # Check if the correct word is found
                if isinstance(self.game.get_state(), WinState):
                    print(f"Number of guesses: {self.num_guesses}")
                    print(f"Solution found: {word}")
                    self.solution_found = True
                    break

                # Continue search if not in Losing state
                if not isinstance(self.game.get_state(), LoseState):
                    self._dfs_search(path + [word])

                # Restore the previous state to backtrack
                if not self.solution_found:
                    self._restore_game_state(saved_state)


    def _make_guess(self, word: str) -> None:
        """
        Simulates typing and entering a word in the game.
        """
        print(f"Inputting word: {word}")
        for letter in word:
            self.game.write_letter(letter)
            pg.display.update()
            print(f"Typed letter: {letter}")

        self.game.enter_word() 
        pg.display.update()
        print(f"Entered word: {word}")

    def _process_feedback(self, word: str) -> None:
        """
        Processes feedback after entering a word to update constraints.
        """
        print("Processing feedback...")
        for i, box in enumerate(self.game.game_matrix[self.game.current_line - 1]):
            letter = box.get_text()
            box_state = box.state 

            if box_state == SUCCESS:
                self.correct_positions[i] = letter
            elif box_state == PARTIAL:
                self.partial_letters.add(letter)
            elif box_state == INCORRECT:
                self.incorrect_letters.add(letter)

        # print(f"Correct positions: {self.correct_positions}")
        # print(f"Partial letters: {self.partial_letters}")
        # print(f"Incorrect letters: {self.incorrect_letters}")

    def _filter_words(self) -> list:
        """
        Filters the list of possible words based on feedback constraints.
        """
        filtered = []
        for word in self.game.word_list:
            if self._matches_constraints(word):
                filtered.append(word)
        # print(f"Filtered words: {filtered}")
        return filtered

    def _matches_constraints(self, word: str) -> bool:
        """
        Checks if a word matches the current constraints.
        """
        # Check correct positions
        for i, letter in enumerate(word):
            if self.correct_positions[i] and self.correct_positions[i] != letter:
                return False
        # Check partial letters
        if not all(letter in word for letter in self.partial_letters):
            return False
        # Check incorrect letters
        if any(letter in word for letter in self.incorrect_letters):
            return False

        return True

    def _save_game_state(self) -> dict:
        """
        Saves the current game state for backtracking.
        """
        print("Saving game state...")
        return {
            'current_line': self.game.current_line,
            'current_letter': self.game.current_letter,
            'game_state': self.game.get_state(),
            'game_matrix': [[box.get_text() for box in row] for row in self.game.game_matrix]
        }

    def _restore_game_state(self, saved_state: dict) -> None:
        """
        Restores the game state from a saved snapshot for backtracking.
        """
        print("Restoring game state...")
        self.game.current_line = saved_state['current_line']
        self.game.current_letter = saved_state['current_letter']
        self.game.game_state = saved_state['game_state']

        # Restore text in boxes
        for i, row in enumerate(saved_state['game_matrix']):
            for j, letter in enumerate(row):
                box = self.game.game_matrix[i][j]
                if letter:
                    box.set_text(letter, self.game.screen)
                else:
                    box.delete_text(self.game.screen)

        pg.display.update() 
        print("Game state restored.")


# Example usage of the DFSWordleSolver class
if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    words_list = open(WORDS_LIST).read()
    words_list = words_list.split('\n')
    words_list = [word.upper() for word in words_list]
    game = Game(screen, WORD_LENGTH, words_list)
    pg.display.update()

    solver = DFS(game)
    solver.solve()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.display.update()
