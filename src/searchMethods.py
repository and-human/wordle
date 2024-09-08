from .constants import *
import pygame as pg
from .gameStates import *
import numpy as np
from collections import Counter, deque

class SearchMethods:
    def __init__(self, game):
        self.game = game
        self.visited = set()  # Track guessed words to avoid repeating guesses
        self.solution_found = False
        self.correct_positions = [''] * game.word_length  # Correct letters in exact positions (green)
        self.partial_letters = {}  # Tracks yellow letters and their explored positions
        self.incorrect_letters = set()  # Letters that are not in the word (black)
        self.num_guesses = 0  # Number of guesses made so far
        self.letter_count = {}  # Counts letters in the target word once it is identified

    def _make_guess(self, word: str) -> None:
        """
        Simulates typing and entering a word in the game.
        """
        print(f"Inputting word: {word}")
        for letter in word:
            pg.time.delay(50)
            self.game.write_letter(letter)
            pg.display.flip()
            print(f"Typed letter: {letter}")

        self.game.enter_word() 
        pg.display.flip()
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
                self.letter_count[letter] = self.letter_count.get(letter, 0) + 1
            elif box_state == PARTIAL:
                if letter not in self.partial_letters:
                    self.partial_letters[letter] = []
                self.partial_letters[letter].append(i)
            elif box_state == INCORRECT:
                self.incorrect_letters.add(letter)

        # print(f"Correct positions: {self.correct_positions}")
        # print(f"Partial letters: {self.partial_letters}")
        # print(f"Incorrect letters: {self.incorrect_letters}")

    def _filter_words(self) -> list:
        """
        Filters the list of possible words based on feedback constraints using the improved filtering logic.
        """
        filtered = []
        for word in self.game.word_list:
            if self._matches_constraints(word):
                filtered.append(word)
        # print(f"Filtered words: {len(filtered)}")
        return filtered

    def _matches_constraints(self, word: str) -> bool:
        """
        Checks if a word matches the current constraints based on updated logic.
        """
        # Check correct positions (green constraints)
        for i, letter in enumerate(word):
            if self.correct_positions[i] and self.correct_positions[i] != letter:
                return False
        
        # Check yellow letters
        for letter, positions in self.partial_letters.items():
            if letter not in word or any(word[i] == letter for i in positions):
                return False
        
        # Check incorrect letters (black constraints)
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
        

class DFS(SearchMethods):
    def __init__(self, game):
        super().__init__(game)
        

    def solve(self):
        """
        Initiates the DFS search to solve the game.
        """
        print("Starting DFS search...")
        self._dfs_search([])
        print("DFS search complete.")

    def _dfs_search(self, path):
        """
        Recursively performs a DFS search to find the target word using feedback.
        """
        if self.solution_found:
            return

        # Save the current state for backtracking
        saved_state = self._save_game_state()

        # Filter the word list based on known constraints using improved logic
        filtered_words = self._filter_words()

        # Iterate over all possible words in the filtered list
        for word in filtered_words:
            if self.solution_found:
                break

            if word not in self.visited:
                self.visited.add(word)
                print(f"Trying word: {word}")
                self.num_guesses += 1

                # Simulate making the guess
                self._make_guess(word)

                if self.num_guesses > ATTEMPTS - 1: 
                    print("Exceeded maximum number of guesses.", self.num_guesses)
                    self.solution_found = True
                    break

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


class BFS(SearchMethods):
    def __init__(self, game):
        super().__init__(game)

    def solve(self):
        """
        Initiates the BFS search to solve the game.
        """
        print("Starting BFS search...")
        self._bfs_search()
        print("BFS search complete.")

    def _bfs_search(self):
        """
        Performs a BFS search to find the target word using feedback.
        """
        # Initialize the queue with the starting row (0) and an empty path
        queue = deque([(0, [])])  

        while queue and not self.solution_found:
            current_row, path = queue.popleft()  # Get the current row and path

            # Ensure we are within the maximum allowed rows
            if current_row >= ATTEMPTS:
                continue

            # Save the current state for backtracking
            saved_state = self._save_game_state()

            # Filter the word list based on known constraints
            filtered_words = self._filter_words()

            # Iterate over all possible words in the filtered list
            for word in filtered_words:
                if self.solution_found:
                    break

                if word not in self.visited:
                    self.visited.add(word)
                    print(f"Trying word: {word} in row {current_row}")
                    self.num_guesses += 1

                    # Set the game's current line to the current row
                    self.game.current_line = current_row

                    # Simulate making the guess
                    self._make_guess(word)

                    if self.num_guesses > ATTEMPTS - 1:
                        print("Exceeded maximum number of guesses.", self.num_guesses)
                        self.solution_found = True
                        break

                    # Process feedback from the guess
                    self._process_feedback(word)

                    # Check if the correct word is found
                    if isinstance(self.game.get_state(), WinState):
                        print(f"Number of guesses: {self.num_guesses}")
                        print(f"Solution found: {word}")
                        self.solution_found = True
                        break

                    # If not in Losing state, add the next row state to the queue
                    if not isinstance(self.game.get_state(), LoseState):
                        next_row = current_row + 1
                        if next_row < ATTEMPTS:
                            queue.append((next_row, path + [word]))

                    # Restore the previous state to backtrack
                    if not self.solution_found:
                        self._restore_game_state(saved_state)




class BestFS(SearchMethods):
    def __init__(self, game):
        super().__init__(game)

    def solve(self):
        """
        Initiates the entropy-based search to solve the game.
        """
        print("Starting Entropy-based search...")
        while not self.solution_found:
            # Filter words based on current knowledge
            filtered_words = self._filter_words()

            if not filtered_words:
                print("No more words to try.")
                break

            # Select the next guess based on maximum entropy
            guess = self._select_best_guess(filtered_words)
            self._make_guess(guess)

            # Process feedback from the guess
            self._process_feedback(guess)

            # Check if the correct word is found
            if isinstance(self.game.get_state(), WinState):
                print(f"Number of guesses: {self.num_guesses}")
                print(f"Solution found: {guess}")
                self.solution_found = True

            # Break if max attempts are reached
            if self.num_guesses > ATTEMPTS - 1:
                print("Exceeded maximum number of guesses.", self.num_guesses)
                break

        print("Entropy-based search complete.")

    def _select_best_guess(self, words):
        """
        Selects the word with the highest expected information gain (entropy).
        """
        max_entropy = -1
        best_guess = None

        for word in words:
            # Calculate the entropy for each possible guess
            entropy = self._calculate_entropy(word, words)
            if entropy > max_entropy:
                max_entropy = entropy
                best_guess = word

        print(f"Selected guess: {best_guess} with entropy: {max_entropy}")
        self.num_guesses += 1
        return best_guess

    def _calculate_entropy(self, guess, candidate_words):
        """
        Calculates the expected entropy of a guess based on the feedback patterns it generates.
        """
        pattern_counts = Counter()

        # Simulate feedback patterns for each candidate word
        for word in candidate_words:
            pattern = self._get_feedback_pattern(guess, word)
            pattern_counts[pattern] += 1

        # Calculate entropy based on pattern distribution
        total = len(candidate_words)
        entropy = 0
        for count in pattern_counts.values():
            prob = count / total
            entropy -= prob * np.log2(prob)

        return entropy

    def _get_feedback_pattern(self, guess, target):
        """
        Generates a feedback pattern as a tuple representing how the guess matches the target.
        Example: ('G', 'Y', '-', '-', '-') for Green, Yellow, and Gray feedback.
        """
        pattern = []
        for g, t in zip(guess, target):
            if g == t:
                pattern.append('G')  # Green (correct position)
            elif g in target:
                pattern.append('Y')  # Yellow (wrong position but correct letter)
            else:
                pattern.append('-')  # Gray (incorrect letter)
        return tuple(pattern)
