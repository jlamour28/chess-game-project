"""
Game constants and configuration settings.
"""

import pygame

# Board settings
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)
LAST_MOVE_COLOR = (255, 255, 0)
CHECK_COLOR = (255, 0, 0)

# AI settings
DEFAULT_DIFFICULTY = "medium"
DIFFICULTY_LEVELS = {
    "easy": {"depth": 2, "time_limit": 1.0},
    "medium": {"depth": 3, "time_limit": 2.0},
    "hard": {"depth": 4, "time_limit": 5.0}
}

# Game settings
ENABLE_SOUNDS = True
ANIMATION_SPEED = 0.1
SHOW_COORDINATES = True

# Piece values for evaluation
PIECE_VALUES = {
    'p': 100, 'P': 100,
    'n': 320, 'N': 320,
    'b': 330, 'B': 330,
    'r': 500, 'R': 500,
    'q': 900, 'Q': 900,
    'k': 20000, 'K': 20000
}

# Fonts
pygame.font.init()
FONT_SIZE = 16
COORDINATE_FONT = pygame.font.SysFont(None, 14)
STATUS_FONT = pygame.font.SysFont(None, 24)
MENU_FONT = pygame.font.SysFont(None, 32)

# Game states
GAME_STATES = {
    "PLAYING": "playing",
    "CHECK": "check",
    "CHECKMATE": "checkmate",
    "STALEMATE": "stalemate",
    "DRAW": "draw"
}

# Player types
PLAYER_TYPES = {
    "HUMAN": "human",
    "AI_MINIMAX": "ai_minimax",
    "AI_STOCKFISH": "ai_stockfish"
}

# Move notation
FILES = 'abcdefgh'
RANKS = '12345678'