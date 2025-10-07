"""
Main entry point for the Chess Game application.
"""

import sys
import os
import pygame

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from game import ChessGame
from ai.minimax import MinimaxAI
from ai.stockfish import StockfishAI
from ui.menu import MainMenu, DifficultyMenu
from ui.game_ui import ChessBoardUI
from utils.constants import *


class GameManager:
    """Manages the overall game flow and mode selection."""

    def __init__(self):
        """Initialize the game manager."""
        self.game = None
        self.ai_opponent = None
        self.game_mode = None

    def start(self):
        """Start the chess game application."""
        # Show main menu
        menu = MainMenu()
        self.game_mode = menu.show()

        if not self.game_mode or self.game_mode == "quit":
            return

        # Initialize game based on selected mode
        self.game = ChessGame()
        self._setup_game_mode()

        # Start the game UI
        if self.game:
            game_ui = ChessBoardUI(self.game)
            game_ui.run()

    def _setup_game_mode(self):
        """Set up the game based on selected mode."""
        if self.game_mode == "human_vs_minimax":
            self._setup_minimax_ai()
        elif self.game_mode == "human_vs_stockfish":
            self._setup_stockfish_ai()
        elif self.game_mode == "human_vs_human":
            self.ai_opponent = None  # No AI for human vs human
        elif self.game_mode == "load_game":
            self._load_saved_game()

    def _setup_minimax_ai(self):
        """Set up minimax AI opponent."""
        difficulty_menu = DifficultyMenu()
        difficulty = difficulty_menu.show("Minimax")

        if difficulty:
            self.ai_opponent = MinimaxAI(difficulty=difficulty)
            print(f"Minimax AI set to {difficulty} difficulty")

    def _setup_stockfish_ai(self):
        """Set up Stockfish AI opponent."""
        difficulty_menu = DifficultyMenu()
        difficulty = difficulty_menu.show("Stockfish")

        if difficulty:
            self.ai_opponent = StockfishAI(difficulty=difficulty)
            if not self.ai_opponent.is_available():
                print("Stockfish not available, falling back to Minimax AI")
                self.ai_opponent = MinimaxAI(difficulty=difficulty)

    def _load_saved_game(self):
        """Load a previously saved game."""
        # This would show a file selection dialog
        # For now, just reset to new game
        pass


def main():
    """Main entry point."""
    try:
        # Initialize pygame
        pygame.init()

        # Create and start game manager
        game_manager = GameManager()
        game_manager.start()

        # Cleanup
        pygame.quit()

    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your installation and try again.")
        pygame.quit()


if __name__ == "__main__":
    main()