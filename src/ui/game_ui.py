"""
Pygame-based graphical user interface for the chess game.
"""

import pygame
import chess
import os
from typing import Optional, Tuple, List
from ..game import ChessGame
from ..utils.constants import *


class ChessBoardUI:
    """
    Pygame UI for the chess board and game interaction.
    """

    def __init__(self, game: ChessGame):
        """
        Initialize the chess board UI.

        Args:
            game: ChessGame instance to display
        """
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode((BOARD_SIZE + 200, BOARD_SIZE))
        pygame.display.set_caption("Chess Game")

        self.selected_square = None
        self.possible_moves: List[chess.Move] = []
        self.dragged_piece = None
        self.drag_offset = (0, 0)

        # Load piece images (if available)
        self.piece_images = self._load_piece_images()

        # Fonts
        self.font = pygame.font.SysFont(None, 20)
        self.small_font = pygame.font.SysFont(None, 16)

        # Game state
        self.running = False
        self.clock = pygame.time.Clock()

    def _load_piece_images(self) -> dict:
        """Load chess piece images from assets folder."""
        images = {}
        piece_symbols = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']

        for symbol in piece_symbols:
            image_path = os.path.join("assets", "pieces", f"{symbol}.png")
            if os.path.exists(image_path):
                images[symbol] = pygame.image.load(image_path)
                # Scale to square size
                images[symbol] = pygame.transform.scale(
                    images[symbol], (SQUARE_SIZE - 10, SQUARE_SIZE - 10)
                )
            else:
                # Fallback to text representation
                images[symbol] = None

        return images

    def run(self):
        """Main game loop."""
        self.running = True

        while self.running:
            self._handle_events()
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_u:  # Undo move
                    self.game.undo_move()
                    self.selected_square = None
                    self.possible_moves.clear()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if self.dragged_piece:
                    self.drag_offset = event.pos

    def _handle_mouse_down(self, pos: Tuple[int, int]):
        """Handle mouse button down events."""
        if pos[0] >= BOARD_SIZE:  # Clicked on side panel
            return

        file = pos[0] // SQUARE_SIZE
        rank = 7 - (pos[1] // SQUARE_SIZE)  # Flip for correct orientation
        square = chess.square(file, rank)

        if self.selected_square is None:
            # Select piece
            piece = self.game.get_piece_at(square)
            if piece and piece.color == self.game.current_player:
                self.selected_square = square
                self.possible_moves = self.game.get_legal_moves(square)

                # Check if piece has an image for dragging
                if piece and piece.symbol() in self.piece_images:
                    self.dragged_piece = piece.symbol()
                    self.drag_offset = pos
        else:
            # Try to make move
            if square in [move.to_square for move in self.possible_moves]:
                # Find the move
                for move in self.possible_moves:
                    if move.to_square == square:
                        if self.game.make_move(move.uci()):
                            self.selected_square = None
                            self.possible_moves.clear()
                        break
            else:
                # Deselect or select new piece
                piece = self.game.get_piece_at(square)
                if piece and piece.color == self.game.current_player:
                    self.selected_square = square
                    self.possible_moves = self.game.get_legal_moves(square)
                else:
                    self.selected_square = None
                    self.possible_moves.clear()

    def _handle_mouse_up(self, pos: Tuple[int, int]):
        """Handle mouse button up events."""
        if self.dragged_piece:
            # Try to drop piece on valid square
            if pos[0] < BOARD_SIZE:
                file = pos[0] // SQUARE_SIZE
                rank = 7 - (pos[1] // SQUARE_SIZE)
                to_square = chess.square(file, rank)

                if self.selected_square is not None:
                    # Try to make move
                    if self.game.make_move_from_squares(self.selected_square, to_square):
                        pass  # Move successful
                    else:
                        # Move failed, snap back to original position
                        pass

            self.dragged_piece = None
            self.selected_square = None
            self.possible_moves.clear()

    def _draw(self):
        """Draw the game interface."""
        self.screen.fill((50, 50, 50))

        # Draw chess board
        self._draw_board()

        # Draw pieces
        self._draw_pieces()

        # Draw highlights
        self._draw_highlights()

        # Draw side panel
        self._draw_side_panel()

        # Draw dragged piece
        if self.dragged_piece and self.drag_offset:
            self._draw_dragged_piece()

    def _draw_board(self):
        """Draw the chess board squares."""
        for rank in range(8):
            for file in range(8):
                x = file * SQUARE_SIZE
                y = (7 - rank) * SQUARE_SIZE  # Flip for correct orientation

                # Determine square color
                if (file + rank) % 2 == 0:
                    color = LIGHT_BROWN
                else:
                    color = DARK_BROWN

                # Draw square
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

                # Draw coordinates (optional)
                if SHOW_COORDINATES:
                    if rank == 7:  # File labels
                        text = self.small_font.render(FILES[file], True, (0, 0, 0))
                        self.screen.blit(text, (x + 2, y + SQUARE_SIZE - 15))
                    if file == 0:  # Rank labels
                        text = self.small_font.render(RANKS[rank], True, (0, 0, 0))
                        self.screen.blit(text, (x + SQUARE_SIZE - 15, y + 2))

    def _draw_pieces(self):
        """Draw chess pieces on the board."""
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, rank)
                piece = self.game.get_piece_at(square)

                if piece:
                    x = file * SQUARE_SIZE + 5
                    y = (7 - rank) * SQUARE_SIZE + 5

                    # Try to use image
                    piece_symbol = piece.symbol()
                    if piece_symbol in self.piece_images and self.piece_images[piece_symbol]:
                        self.screen.blit(self.piece_images[piece_symbol], (x, y))
                    else:
                        # Fallback to text
                        color = (0, 0, 0) if piece.color == chess.BLACK else (255, 255, 255)
                        text = self.font.render(piece_symbol, True, color)
                        self.screen.blit(text, (x + 10, y + 5))

    def _draw_highlights(self):
        """Draw highlights for selected squares and possible moves."""
        # Highlight selected square
        if self.selected_square is not None:
            file = chess.square_file(self.selected_square)
            rank = chess.square_rank(self.selected_square)
            x = file * SQUARE_SIZE
            y = (7 - rank) * SQUARE_SIZE

            highlight_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            highlight_surf.set_alpha(128)
            highlight_surf.fill(HIGHLIGHT_COLOR)
            self.screen.blit(highlight_surf, (x, y))

        # Highlight possible moves
        for move in self.possible_moves:
            file = chess.square_file(move.to_square)
            rank = chess.square_rank(move.to_square)
            x = file * SQUARE_SIZE
            y = (7 - rank) * SQUARE_SIZE

            # Draw circle for possible moves
            center_x = x + SQUARE_SIZE // 2
            center_y = y + SQUARE_SIZE // 2
            pygame.draw.circle(self.screen, HIGHLIGHT_COLOR, (center_x, center_y), 15)

        # Highlight last move
        if self.game.last_move:
            from_file = chess.square_file(self.game.last_move.from_square)
            from_rank = chess.square_rank(self.game.last_move.from_square)
            to_file = chess.square_file(self.game.last_move.to_square)
            to_rank = chess.square_rank(self.game.last_move.to_square)

            # From square
            x1 = from_file * SQUARE_SIZE
            y1 = (7 - from_rank) * SQUARE_SIZE
            # To square
            x2 = to_file * SQUARE_SIZE
            y2 = (7 - to_rank) * SQUARE_SIZE

            last_move_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            last_move_surf.set_alpha(100)
            last_move_surf.fill(LAST_MOVE_COLOR)

            self.screen.blit(last_move_surf, (x1, y1))
            self.screen.blit(last_move_surf, (x2, y2))

        # Highlight check
        if self.game.is_check():
            king_square = self.game.board.king(self.game.current_player)
            if king_square:
                file = chess.square_file(king_square)
                rank = chess.square_rank(king_square)
                x = file * SQUARE_SIZE
                y = (7 - rank) * SQUARE_SIZE

                check_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                check_surf.set_alpha(150)
                check_surf.fill(CHECK_COLOR)
                self.screen.blit(check_surf, (x, y))

    def _draw_side_panel(self):
        """Draw the side panel with game information."""
        panel_x = BOARD_SIZE
        panel_width = 200

        # Panel background
        pygame.draw.rect(self.screen, (40, 40, 40), (panel_x, 0, panel_width, BOARD_SIZE))

        # Game status
        status_text = self.game.get_game_status_text()
        status_surf = self.font.render(status_text, True, (255, 255, 255))
        self.screen.blit(status_surf, (panel_x + 10, 10))

        # Current player
        current_player = "White" if self.game.current_player == chess.WHITE else "Black"
        player_text = f"Turn: {current_player}"
        player_surf = self.small_font.render(player_text, True, (200, 200, 200))
        self.screen.blit(player_surf, (panel_x + 10, 40))

        # Move history
        self._draw_move_history(panel_x + 10, 70)

        # Controls
        controls_text = "ESC: Quit | U: Undo"
        controls_surf = self.small_font.render(controls_text, True, (150, 150, 150))
        self.screen.blit(controls_surf, (panel_x + 10, BOARD_SIZE - 30))

    def _draw_move_history(self, x: int, y: int):
        """Draw the move history in the side panel."""
        history_title = self.small_font.render("Move History:", True, (200, 200, 200))
        self.screen.blit(history_title, (x, y))

        for i, move in enumerate(self.game.move_history[-10:]):  # Last 10 moves
            move_text = f"{i+1}. {move}"
            move_surf = self.small_font.render(move_text, True, (180, 180, 180))
            self.screen.blit(move_surf, (x, y + 20 + i * 18))

    def _draw_dragged_piece(self):
        """Draw the piece being dragged."""
        if self.dragged_piece and self.drag_offset:
            # Get piece image
            if self.dragged_piece in self.piece_images and self.piece_images[self.dragged_piece]:
                image = self.piece_images[self.dragged_piece]
                # Draw with offset for better visual feedback
                drag_x = self.drag_offset[0] - SQUARE_SIZE // 2
                drag_y = self.drag_offset[1] - SQUARE_SIZE // 2
                self.screen.blit(image, (drag_x, drag_y))
            else:
                # Fallback to text
                color = (0, 0, 0) if self.dragged_piece.islower() else (255, 255, 255)
                text = self.font.render(self.dragged_piece, True, color)
                self.screen.blit(text, self.drag_offset)