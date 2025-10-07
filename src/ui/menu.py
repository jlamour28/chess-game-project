"""
Main menu and game mode selection interface.
"""

import pygame
import sys
from typing import Tuple, Optional
from ..utils.constants import *


class MenuButton:
    """Simple button class for menu interface."""

    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 color: Tuple[int, int, int] = (200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (150, 150, 150)
        self.current_color = color

    def draw(self, screen: pygame.Surface):
        """Draw the button on screen."""
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border

        # Draw text
        font = pygame.font.SysFont(None, 24)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events for the button."""
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class MainMenu:
    """Main menu for the chess game."""

    def __init__(self):
        """Initialize the main menu."""
        self.screen = None
        self.running = False

        # Menu options
        self.buttons = []
        self.selected_option = None

    def show(self) -> Optional[str]:
        """
        Display the main menu.

        Returns:
            Selected menu option or None if cancelled
        """
        pygame.init()
        self.screen = pygame.display.set_mode((400, 500))
        pygame.display.set_caption("Chess Game - Main Menu")

        # Create buttons
        self._create_buttons()

        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    self._handle_button_events(event)

            self._draw()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        return self.selected_option

    def _create_buttons(self):
        """Create menu buttons."""
        button_width = 200
        button_height = 40
        start_x = (400 - button_width) // 2
        start_y = 150

        buttons_data = [
            ("Human vs Minimax AI", "human_vs_minimax"),
            ("Human vs Stockfish", "human_vs_stockfish"),
            ("Human vs Human", "human_vs_human"),
            ("Load Saved Game", "load_game"),
            ("Settings", "settings"),
            ("Quit", "quit")
        ]

        for i, (text, option) in enumerate(buttons_data):
            button = MenuButton(
                start_x,
                start_y + i * 50,
                button_width,
                button_height,
                text
            )
            button.option = option
            self.buttons.append(button)

    def _handle_button_events(self, event: pygame.event.Event):
        """Handle events for all buttons."""
        for button in self.buttons:
            if button.handle_event(event):
                self.selected_option = button.option
                if button.option == "quit":
                    pygame.quit()
                    sys.exit()
                else:
                    self.running = False

    def _draw(self):
        """Draw the menu screen."""
        self.screen.fill((50, 50, 50))

        # Title
        title_font = pygame.font.SysFont(None, 48)
        title_text = title_font.render("Chess Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(200, 80))
        self.screen.blit(title_text, title_rect)

        # Subtitle
        subtitle_font = pygame.font.SysFont(None, 20)
        subtitle_text = subtitle_font.render("Choose Game Mode", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(200, 120))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        # Instructions
        inst_font = pygame.font.SysFont(None, 16)
        inst_text = inst_font.render("Use mouse to select option", True, (150, 150, 150))
        inst_rect = inst_text.get_rect(center=(200, 450))
        self.screen.blit(inst_text, inst_rect)


class DifficultyMenu:
    """Menu for selecting AI difficulty."""

    def __init__(self):
        """Initialize difficulty selection menu."""
        self.screen = None
        self.running = False
        self.buttons = []
        self.selected_difficulty = None

    def show(self, ai_type: str) -> Optional[str]:
        """
        Display difficulty selection menu.

        Args:
            ai_type: Type of AI ('minimax' or 'stockfish')

        Returns:
            Selected difficulty level or None if cancelled
        """
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption(f"Select {ai_type.title()} Difficulty")

        self._create_buttons(ai_type)
        self.running = True

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    self._handle_button_events(event)

            self._draw(ai_type)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        return self.selected_difficulty

    def _create_buttons(self, ai_type: str):
        """Create difficulty selection buttons."""
        button_width = 150
        button_height = 40
        start_x = (400 - button_width) // 2
        start_y = 150

        difficulties = ["easy", "medium", "hard"]

        for i, difficulty in enumerate(difficulties):
            button = MenuButton(
                start_x,
                start_y + i * 60,
                button_width,
                button_height,
                difficulty.title()
            )
            button.difficulty = difficulty
            self.buttons.append(button)

        # Back button
        back_button = MenuButton(50, 320, 100, 30, "Back", (150, 150, 150))
        back_button.difficulty = "back"
        self.buttons.append(back_button)

    def _handle_button_events(self, event: pygame.event.Event):
        """Handle events for difficulty buttons."""
        for button in self.buttons:
            if button.handle_event(event):
                if button.difficulty == "back":
                    self.running = False
                else:
                    self.selected_difficulty = button.difficulty
                    self.running = False

    def _draw(self, ai_type: str):
        """Draw the difficulty selection screen."""
        self.screen.fill((50, 50, 50))

        # Title
        title_font = pygame.font.SysFont(None, 32)
        title_text = title_font.render(f"{ai_type.title()} Difficulty", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(200, 60))
        self.screen.blit(title_text, title_rect)

        # Description
        desc_font = pygame.font.SysFont(None, 18)
        desc_text = desc_font.render("Easy: Fast, Medium: Balanced, Hard: Strong", True, (200, 200, 200))
        desc_rect = desc_text.get_rect(center=(200, 100))
        self.screen.blit(desc_text, desc_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)