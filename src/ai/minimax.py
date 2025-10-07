"""
Minimax AI implementation with alpha-beta pruning for chess.
"""

import chess
import random
import time
from typing import Tuple, Optional
from ..utils.constants import PIECE_VALUES, DIFFICULTY_LEVELS


class MinimaxAI:
    """
    Minimax AI with alpha-beta pruning for chess.
    """

    def __init__(self, difficulty: str = "medium"):
        """
        Initialize the AI.

        Args:
            difficulty: Difficulty level ('easy', 'medium', 'hard')
        """
        self.difficulty = difficulty
        self.depth = DIFFICULTY_LEVELS[difficulty]["depth"]
        self.time_limit = DIFFICULTY_LEVELS[difficulty]["time_limit"]

        # Transposition table for optimization
        self.transposition_table = {}
        self.table_hits = 0

    def get_best_move(self, board: chess.Board) -> Optional[str]:
        """
        Get the best move using minimax algorithm.

        Args:
            board: Current chess board position

        Returns:
            Best move in UCI notation, or None if no moves available
        """
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        # Shuffle moves for variety at same evaluation
        random.shuffle(legal_moves)

        start_time = time.time()
        best_move = None
        best_value = float('-inf')

        # Iterative deepening for time management
        for depth in range(1, self.depth + 1):
            if time.time() - start_time > self.time_limit:
                break

            current_best_move = None
            current_best_value = float('-inf')

            for move in legal_moves:
                board.push(move)
                value = self._minimax(board, depth - 1, False, float('-inf'), float('inf'), start_time)
                board.pop()

                if value > current_best_value:
                    current_best_value = value
                    current_best_move = move

            if current_best_move:
                best_move = current_best_move
                best_value = current_best_value

        return best_move.uci() if best_move else legal_moves[0].uci()

    def _minimax(self, board: chess.Board, depth: int, maximizing: bool,
                 alpha: float, beta: float, start_time: float) -> float:
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            board: Current board position
            depth: Search depth remaining
            maximizing: True if maximizing player (AI)
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            start_time: Time when search started

        Returns:
            Evaluation value of the position
        """
        # Check time limit
        if time.time() - start_time > self.time_limit:
            return 0

        # Check transposition table
        board_key = board.fen()
        if board_key in self.transposition_table:
            cached_value, cached_depth = self.transposition_table[board_key]
            if cached_depth >= depth:
                self.table_hits += 1
                return cached_value

        # Terminal nodes
        if depth == 0 or board.is_game_over():
            return self._evaluate_position(board)

        legal_moves = list(board.legal_moves)

        if maximizing:
            max_value = float('-inf')
            for move in legal_moves:
                board.push(move)
                value = self._minimax(board, depth - 1, False, alpha, beta, start_time)
                board.pop()

                max_value = max(max_value, value)
                alpha = max(alpha, value)

                if beta <= alpha:
                    break  # Alpha-beta pruning

            # Cache result
            self.transposition_table[board_key] = (max_value, depth)
            return max_value
        else:
            min_value = float('inf')
            for move in legal_moves:
                board.push(move)
                value = self._minimax(board, depth - 1, True, alpha, beta, start_time)
                board.pop()

                min_value = min(min_value, value)
                beta = min(beta, value)

                if beta <= alpha:
                    break  # Alpha-beta pruning

            # Cache result
            self.transposition_table[board_key] = (min_value, depth)
            return min_value

    def _evaluate_position(self, board: chess.Board) -> float:
        """
        Evaluate the current position.

        Args:
            board: Board position to evaluate

        Returns:
            Position evaluation from AI's perspective
        """
        if board.is_checkmate():
            return float('-inf') if board.turn == chess.WHITE else float('inf')

        if board.is_stalemate():
            return 0

        evaluation = 0

        # Material evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = PIECE_VALUES[piece.symbol()]
                if piece.color == chess.WHITE:
                    evaluation += value
                else:
                    evaluation -= value

        # Positional evaluation (simplified)
        evaluation += self._positional_bonus(board)

        # Mobility bonus
        evaluation += self._mobility_bonus(board)

        # King safety
        evaluation += self._king_safety(board)

        return evaluation if board.turn == chess.WHITE else -evaluation

    def _positional_bonus(self, board: chess.Board) -> float:
        """Simple positional bonuses for pieces."""
        bonus = 0

        # Center control bonus
        center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
        for square in center_squares:
            piece = board.piece_at(square)
            if piece and piece.piece_type != chess.KING:
                bonus += 10 if piece.color == chess.WHITE else -10

        return bonus

    def _mobility_bonus(self, board: chess.Board) -> float:
        """Bonus for having more legal moves."""
        our_moves = len(list(board.legal_moves))
        board.push(chess.Move.null())  # Switch turns
        their_moves = len(list(board.legal_moves))
        board.pop()

        return (our_moves - their_moves) * 2

    def _king_safety(self, board: chess.Board) -> float:
        """Simple king safety evaluation."""
        safety = 0

        # Penalty for exposed king
        for color in [chess.WHITE, chess.BLACK]:
            king_square = board.king(color)
            if king_square:
                # Count attackers
                attackers = 0
                for square in chess.SQUARES:
                    piece = board.piece_at(square)
                    if (piece and piece.color != color and
                        square != king_square and
                        board.is_attacked_by(piece.color, king_square)):
                        attackers += 1

                if color == chess.WHITE:
                    safety -= attackers * 5
                else:
                    safety += attackers * 5

        return safety

    def set_difficulty(self, difficulty: str):
        """Change the AI difficulty level."""
        if difficulty in DIFFICULTY_LEVELS:
            self.difficulty = difficulty
            self.depth = DIFFICULTY_LEVELS[difficulty]["depth"]
            self.time_limit = DIFFICULTY_LEVELS[difficulty]["time_limit"]

    def clear_cache(self):
        """Clear the transposition table."""
        self.transposition_table.clear()
        self.table_hits = 0

    def get_stats(self) -> dict:
        """Get AI performance statistics."""
        total_positions = len(self.transposition_table) + self.table_hits
        hit_rate = (self.table_hits / total_positions * 100) if total_positions > 0 else 0

        return {
            'difficulty': self.difficulty,
            'search_depth': self.depth,
            'cache_size': len(self.transposition_table),
            'cache_hits': self.table_hits,
            'hit_rate': round(hit_rate, 2)
        }