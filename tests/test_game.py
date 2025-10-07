"""
Unit tests for the chess game logic.
"""

import unittest
import chess
from src.game import ChessGame


class TestChessGame(unittest.TestCase):
    """Test cases for ChessGame class."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = ChessGame()

    def test_initial_position(self):
        """Test that game starts in correct initial position."""
        self.assertEqual(self.game.current_player, chess.WHITE)
        self.assertEqual(self.game.game_state, "playing")
        self.assertFalse(self.game.is_check())
        self.assertEqual(len(self.game.move_history), 0)

    def test_make_valid_move(self):
        """Test making a valid move."""
        # e2e4 (pawn to e4)
        success = self.game.make_move("e2e4")
        self.assertTrue(success)
        self.assertEqual(self.game.current_player, chess.BLACK)
        self.assertEqual(len(self.game.move_history), 1)
        self.assertEqual(self.game.move_history[0], "e2e4")

    def test_make_invalid_move(self):
        """Test that invalid moves are rejected."""
        # Invalid move (pawn can't move to e5 from e2)
        success = self.game.make_move("e2e5")
        self.assertFalse(success)
        self.assertEqual(self.game.current_player, chess.WHITE)  # Should not change

    def test_undo_move(self):
        """Test undoing moves."""
        # Make a move
        self.game.make_move("e2e4")
        self.assertEqual(len(self.game.move_history), 1)

        # Undo the move
        success = self.game.undo_move()
        self.assertTrue(success)
        self.assertEqual(len(self.game.move_history), 0)
        self.assertEqual(self.game.current_player, chess.WHITE)

    def test_check_detection(self):
        """Test check detection."""
        # Set up a position where white is in check
        self.game.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        self.assertTrue(self.game.is_check())

    def test_checkmate_detection(self):
        """Test checkmate detection."""
        # Fool's mate position
        self.game.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1")
        self.assertTrue(self.game.is_checkmate())

    def test_game_over_conditions(self):
        """Test various game over conditions."""
        # Stalemate position
        self.game.load_from_fen("7k/8/8/8/8/8/8/K7 w - - 0 1")
        self.assertTrue(self.game.is_stalemate())
        self.assertTrue(self.game.is_game_over())

    def test_save_load_game(self):
        """Test saving and loading game state."""
        # Make some moves
        self.game.make_move("e2e4")
        self.game.make_move("e7e5")

        # Save game
        filename = "test_game.json"
        success = self.game.save_game(filename)
        self.assertTrue(success)

        # Create new game and load
        new_game = ChessGame()
        success = new_game.load_game(filename)
        self.assertTrue(success)
        self.assertEqual(new_game.move_history, self.game.move_history)
        self.assertEqual(new_game.current_player, self.game.current_player)

        # Cleanup
        import os
        if os.path.exists(filename):
            os.remove(filename)

    def test_get_legal_moves(self):
        """Test getting legal moves for a square."""
        # Get moves for e2 pawn
        e2_square = chess.square(4, 1)  # e2
        moves = self.game.get_legal_moves(e2_square)

        self.assertTrue(len(moves) > 0)

        # Should include e4 move
        e4_move = chess.Move.from_uci("e2e4")
        self.assertIn(e4_move, moves)

    def test_piece_at_square(self):
        """Test getting piece at specific square."""
        # Check initial position pieces
        e2_square = chess.square(4, 1)  # e2
        piece = self.game.get_piece_at(e2_square)

        self.assertIsNotNone(piece)
        self.assertEqual(piece.piece_type, chess.PAWN)
        self.assertEqual(piece.color, chess.WHITE)


if __name__ == '__main__':
    unittest.main()