"""
Core chess game logic and state management.
"""

import chess
import json
import os
from typing import List, Tuple, Optional
from .utils.constants import *


class ChessGame:
    """
    Main chess game class that manages game state, moves, and rules.
    """

    def __init__(self):
        """Initialize a new chess game."""
        self.board = chess.Board()
        self.move_history: List[str] = []
        self.game_state = GAME_STATES["PLAYING"]
        self.current_player = chess.WHITE
        self.selected_square = None
        self.possible_moves: List[chess.Move] = []
        self.last_move = None

    def make_move(self, move: str) -> bool:
        """
        Make a move on the board.

        Args:
            move (str): Move in UCI notation (e.g., 'e2e4')

        Returns:
            bool: True if move was successful, False otherwise
        """
        try:
            chess_move = chess.Move.from_uci(move)
            if chess_move in self.board.legal_moves:
                # Store last move for highlighting
                self.last_move = chess_move

                # Make the move
                self.board.push(chess_move)

                # Update game state
                self._update_game_state()

                # Add to history
                self.move_history.append(move)

                # Switch players
                self.current_player = not self.current_player

                return True
            return False
        except ValueError:
            return False

    def make_move_from_squares(self, from_square: chess.Square, to_square: chess.Square) -> bool:
        """
        Make a move using square indices.

        Args:
            from_square: Starting square index (0-63)
            to_square: Ending square index (0-63)

        Returns:
            bool: True if move was successful, False otherwise
        """
        try:
            move = chess.Move(from_square, to_square)
            if move in self.board.legal_moves:
                return self.make_move(move.uci())
            # Try promotion moves
            for legal_move in self.board.legal_moves:
                if (legal_move.from_square == from_square and
                    legal_move.to_square == to_square):
                    return self.make_move(legal_move.uci())
            return False
        except Exception:
            return False

    def get_legal_moves(self, square: Optional[chess.Square] = None) -> List[chess.Move]:
        """
        Get legal moves for a specific square or all legal moves.

        Args:
            square: Square to get moves for, or None for all moves

        Returns:
            List of legal moves
        """
        if square is not None:
            return [move for move in self.board.legal_moves if move.from_square == square]
        return list(self.board.legal_moves)

    def is_check(self) -> bool:
        """Check if current player is in check."""
        return self.board.is_check()

    def is_checkmate(self) -> bool:
        """Check if current player is in checkmate."""
        return self.board.is_checkmate()

    def is_stalemate(self) -> bool:
        """Check if game is in stalemate."""
        return self.board.is_stalemate()

    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.board.is_game_over()

    def get_winner(self) -> Optional[str]:
        """
        Get the winner of the game.

        Returns:
            'white', 'black', or None if game not over
        """
        if self.board.is_checkmate():
            return 'black' if self.current_player else 'white'
        return None

    def _update_game_state(self):
        """Update the current game state."""
        if self.board.is_checkmate():
            self.game_state = GAME_STATES["CHECKMATE"]
        elif self.board.is_stalemate():
            self.game_state = GAME_STATES["STALEMATE"]
        elif self.board.is_check():
            self.game_state = GAME_STATES["CHECK"]
        elif self.board.is_game_over():
            self.game_state = GAME_STATES["DRAW"]
        else:
            self.game_state = GAME_STATES["PLAYING"]

    def get_board_fen(self) -> str:
        """Get the current board position in FEN notation."""
        return self.board.fen()

    def load_from_fen(self, fen: str) -> bool:
        """
        Load a board position from FEN notation.

        Args:
            fen: FEN string representing board position

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.board = chess.Board(fen)
            self.move_history.clear()
            self._update_game_state()
            self.current_player = chess.WHITE if self.board.turn else chess.BLACK
            return True
        except Exception:
            return False

    def undo_move(self) -> bool:
        """
        Undo the last move.

        Returns:
            bool: True if successful, False if no moves to undo
        """
        if self.board.move_stack:
            self.board.pop()
            if self.move_history:
                self.move_history.pop()

            # Update state
            self._update_game_state()
            self.current_player = not self.current_player
            self.last_move = None

            # Clear selection
            self.selected_square = None
            self.possible_moves.clear()

            return True
        return False

    def reset_game(self):
        """Reset the game to starting position."""
        self.board = chess.Board()
        self.move_history.clear()
        self.game_state = GAME_STATES["PLAYING"]
        self.current_player = chess.WHITE
        self.selected_square = None
        self.possible_moves.clear()
        self.last_move = None

    def get_piece_at(self, square: chess.Square) -> Optional[chess.Piece]:
        """Get the piece at a specific square."""
        return self.board.piece_at(square)

    def is_square_attacked(self, square: chess.Square, by_color: chess.Color) -> bool:
        """
        Check if a square is attacked by a specific color.

        Args:
            square: Square to check
            by_color: Color to check attacks from

        Returns:
            bool: True if square is attacked
        """
        return self.board.is_attacked_by(by_color, square)

    def save_game(self, filename: str) -> bool:
        """
        Save the current game state to a file.

        Args:
            filename: Path to save file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            game_data = {
                'fen': self.board.fen(),
                'move_history': self.move_history,
                'current_player': self.current_player,
                'game_state': self.game_state
            }

            with open(filename, 'w') as f:
                json.dump(game_data, f)
            return True
        except Exception:
            return False

    def load_game(self, filename: str) -> bool:
        """
        Load a game state from a file.

        Args:
            filename: Path to save file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(filename):
                return False

            with open(filename, 'r') as f:
                game_data = json.load(f)

            self.load_from_fen(game_data['fen'])
            self.move_history = game_data.get('move_history', [])
            self.current_player = game_data.get('current_player', chess.WHITE)
            self.game_state = game_data.get('game_state', GAME_STATES["PLAYING"])

            return True
        except Exception:
            return False

    def get_game_status_text(self) -> str:
        """Get a human-readable game status message."""
        if self.game_state == GAME_STATES["CHECKMATE"]:
            winner = self.get_winner()
            return f"Checkmate! {winner.title()} wins!"
        elif self.game_state == GAME_STATES["STALEMATE"]:
            return "Stalemate! It's a draw."
        elif self.game_state == GAME_STATES["DRAW"]:
            return "Draw!"
        elif self.game_state == GAME_STATES["CHECK"]:
            return "Check!"
        else:
            current_player = "White" if self.current_player else "Black"
            return f"{current_player} to move"

    def __str__(self) -> str:
        """String representation of the board."""
        return str(self.board)