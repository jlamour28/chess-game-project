"""
Unit tests for AI implementations.
"""

import unittest
import chess
from src.ai.minimax import MinimaxAI
from src.ai.stockfish import StockfishAI


class TestMinimaxAI(unittest.TestCase):
    """Test cases for MinimaxAI class."""

    def setUp(self):
        """Set up test fixtures."""
        self.ai = MinimaxAI(difficulty="easy")
        self.game = chess.Board()

    def test_initialization(self):
        """Test AI initialization."""
        self.assertEqual(self.ai.difficulty, "easy")
        self.assertEqual(self.ai.depth, 2)  # Easy difficulty depth

        # Test different difficulties
        medium_ai = MinimaxAI(difficulty="medium")
        self.assertEqual(medium_ai.depth, 3)

        hard_ai = MinimaxAI(difficulty="hard")
        self.assertEqual(hard_ai.depth, 4)

    def test_get_best_move(self):
        """Test getting best move from AI."""
        move = self.ai.get_best_move(self.game)

        self.assertIsNotNone(move)
        self.assertIsInstance(move, str)

        # Should be a valid UCI move
        try:
            chess.Move.from_uci(move)
        except ValueError:
            self.fail(f"Invalid UCI move: {move}")

    def test_evaluate_position(self):
        """Test position evaluation."""
        # Test initial position
        evaluation = self.ai._evaluate_position(self.game)
        self.assertIsInstance(evaluation, float)

        # Test checkmate position (should be very negative for AI as white)
        checkmate_board = chess.Board("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1")
        mate_eval = self.ai._evaluate_position(checkmate_board)
        self.assertTrue(mate_eval < -1000)  # Very bad for white

    def test_difficulty_change(self):
        """Test changing AI difficulty."""
        self.ai.set_difficulty("hard")
        self.assertEqual(self.ai.difficulty, "hard")
        self.assertEqual(self.ai.depth, 4)

    def test_cache_functionality(self):
        """Test transposition table functionality."""
        # Clear cache
        self.ai.clear_cache()
        self.assertEqual(len(self.ai.transposition_table), 0)

        # Make some moves and check cache grows
        initial_cache_size = len(self.ai.transposition_table)
        self.ai.get_best_move(self.game)
        final_cache_size = len(self.ai.transposition_table)

        self.assertGreaterEqual(final_cache_size, initial_cache_size)

    def test_stats(self):
        """Test AI statistics."""
        stats = self.ai.get_stats()
        expected_keys = ['difficulty', 'search_depth', 'cache_size', 'cache_hits', 'hit_rate']

        for key in expected_keys:
            self.assertIn(key, stats)

        self.assertEqual(stats['difficulty'], 'easy')
        self.assertEqual(stats['search_depth'], 2)


class TestStockfishAI(unittest.TestCase):
    """Test cases for StockfishAI class."""

    def setUp(self):
        """Set up test fixtures."""
        self.ai = StockfishAI(difficulty="easy")
        self.game = chess.Board()

    def test_initialization(self):
        """Test AI initialization."""
        self.assertEqual(self.ai.difficulty, "easy")
        self.assertEqual(self.ai.skill_level, 5)  # Easy skill level

    def test_find_stockfish(self):
        """Test Stockfish executable detection."""
        # This might fail if Stockfish is not installed
        path = self.ai._find_stockfish()
        if path:
            self.assertIsNotNone(path)
            self.assertTrue(isinstance(path, str))

    def test_skill_level_mapping(self):
        """Test skill level mapping for difficulties."""
        easy_ai = StockfishAI(difficulty="easy")
        self.assertEqual(easy_ai.skill_level, 5)

        medium_ai = StockfishAI(difficulty="medium")
        self.assertEqual(medium_ai.skill_level, 10)

        hard_ai = StockfishAI(difficulty="hard")
        self.assertEqual(hard_ai.skill_level, 20)

    def test_availability_check(self):
        """Test checking if Stockfish is available."""
        # If Stockfish is not available, this should return False
        available = self.ai.is_available()
        self.assertIsInstance(available, bool)

    def test_get_best_move_unavailable(self):
        """Test getting move when Stockfish is not available."""
        if not self.ai.is_available():
            move = self.ai.get_best_move(self.game)
            self.assertIsNone(move)  # Should return None if not available

    def test_difficulty_change(self):
        """Test changing difficulty."""
        self.ai.set_difficulty("hard")
        self.assertEqual(self.ai.difficulty, "hard")
        self.assertEqual(self.ai.skill_level, 20)

    def test_engine_info(self):
        """Test getting engine information."""
        info = self.ai.get_engine_info()
        expected_keys = ['available', 'path', 'difficulty', 'skill_level']

        for key in expected_keys:
            self.assertIn(key, info)

    def test_quit_engine(self):
        """Test quitting the engine."""
        # This should not raise an exception
        try:
            self.ai.quit()
        except Exception as e:
            self.fail(f"quit() raised an exception: {e}")


class TestAISpeed(unittest.TestCase):
    """Test AI performance and speed."""

    def test_minimax_speed(self):
        """Test that minimax AI responds within reasonable time."""
        import time

        ai = MinimaxAI(difficulty="easy")
        game = chess.Board()

        start_time = time.time()
        move = ai.get_best_move(game)
        end_time = time.time()

        # Should respond within 5 seconds even on easy
        self.assertLess(end_time - start_time, 5.0)
        self.assertIsNotNone(move)

    def test_stockfish_speed(self):
        """Test that Stockfish AI responds within reasonable time."""
        import time

        ai = StockfishAI(difficulty="easy")

        if ai.is_available():
            game = chess.Board()

            start_time = time.time()
            move = ai.get_best_move(game)
            end_time = time.time()

            # Should respond within 3 seconds
            self.assertLess(end_time - start_time, 3.0)
            if move:  # Only check if we got a move
                self.assertIsInstance(move, str)


if __name__ == '__main__':
    unittest.main()