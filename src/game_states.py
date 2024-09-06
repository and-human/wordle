from .constants import *

class GameState:
    """
    Base class for game states
    """
    def __init__(self):
        self.text = None
        self.background_color = None
        self.finished = False

class PlayState(GameState):
    """
    Play state of the game
    """
    def __init__(self):
        super().__init__()
        self.text = "Playing"
        self.background_color = BG_COLOR
        self.finished = False

class WinState(GameState):
    """
    Win state of the game
    """
    def __init__(self):
        super().__init__()
        self.text = "You Win!"
        self.background_color = SUCCESS_BOX_COLOR
        self.finished = True

class LoseState(GameState):
    """
    Lose state of the game
    """
    def __init__(self):
        super().__init__()
        self.text = "You Lose!"
        self.background_color = INCORRECT_BOX_COLOR
        self.finished = True

class WordNotFound(GameState):
    """
    Word not found state
    """
    def __init__(self):
        super().__init__()
        self.text = "Word not found"
        self.background_color = BG_COLOR
        self.finished = False