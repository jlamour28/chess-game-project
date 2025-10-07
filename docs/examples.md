# Chess Game - Code Examples

This document provides practical examples of how to use the chess game components in your own code.

## Basic Game Usage

```python
from src.game import ChessGame
from src.ai.minimax import MinimaxAI

# Create a new game
game = ChessGame()

# Make moves
game.make_move("e2e4")  # White pawn to e4
game.make_move("e7e5")  # Black pawn to e5
game.make_move("g1f3")  # White knight to f3

print(f"Current player: {'White' if game.current_player else 'Black'}")
print(f"Game status: {game.get_game_status_text()}")
print(f"Move history: {game.move_history}")
```

## Using the Minimax AI

```python
from src.game import ChessGame
from src.ai.minimax import MinimaxAI

# Create game and AI
game = ChessGame()
ai = MinimaxAI(difficulty="medium")

# Human makes a move
game.make_move("e2e4")

# AI calculates and makes a move
ai_move = ai.get_best_move(game.board)
if ai_move:
    game.make_move(ai_move)
    print(f"AI played: {ai_move}")

# Get AI statistics
stats = ai.get_stats()
print(f"AI searched {stats['cache_size']} positions")
```

## Using Stockfish AI

```python
from src.game import ChessGame
from src.ai.stockfish import StockfishAI

# Create game and Stockfish AI
game = ChessGame()
ai = StockfishAI(difficulty="hard")

# Check if Stockfish is available
if ai.is_available():
    # Get the best move
    move = ai.get_best_move(game.board)
    if move:
        game.make_move(move)
        print(f"Stockfish suggests: {move}")
else:
    print("Stockfish not available")
```

## Save and Load Games

```python
from src.game import ChessGame
from src.utils.save_load import save_game, load_game

# Create and play a game
game = ChessGame()
game.make_move("e2e4")
game.make_move("e7e5")

# Save the game
save_game(game, "my_chess_game.json")

# Later, load the game
loaded_game = load_game("my_chess_game.json")
print(f"Loaded game with {len(loaded_game.move_history)} moves")
```

## Custom AI Implementation

```python
from src.ai.minimax import MinimaxAI
import chess

class MyCustomAI(MinimaxAI):
    def _evaluate_position(self, board):
        """Custom evaluation function."""
        if board.is_checkmate():
            return float('-inf') if board.turn == chess.WHITE else float('inf')

        evaluation = super()._evaluate_position(board)

        # Add custom evaluation logic here
        # For example, bonus for controlling the center
        center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
        for square in center_squares:
            piece = board.piece_at(square)
            if piece and piece.piece_type != chess.KING:
                evaluation += 50 if piece.color == chess.WHITE else -50

        return evaluation
```

## Pygame Integration Example

```python
import pygame
from src.game import ChessGame
from src.ui.game_ui import ChessBoardUI

# Initialize Pygame
pygame.init()

# Create game
game = ChessGame()

# Create and run UI
game_ui = ChessBoardUI(game)
game_ui.run()

# Cleanup
pygame.quit()
```

## Testing Your Code

```python
import unittest
from src.game import ChessGame

class TestMyChessCode(unittest.TestCase):
    def test_game_creation(self):
        game = ChessGame()
        self.assertEqual(len(game.move_history), 0)
        self.assertFalse(game.is_game_over())

    def test_opening_moves(self):
        game = ChessGame()
        self.assertTrue(game.make_move("e2e4"))
        self.assertTrue(game.make_move("e7e5"))
        self.assertEqual(len(game.move_history), 2)

if __name__ == '__main__':
    unittest.main()
```

## Performance Optimization

```python
from src.ai.minimax import MinimaxAI

# For faster AI on slower computers
ai = MinimaxAI(difficulty="easy")  # Lower depth
ai.set_difficulty("easy")

# Clear cache periodically to save memory
ai.clear_cache()

# Get performance stats
stats = ai.get_stats()
print(f"Cache hit rate: {stats['hit_rate']}%")
```

## Error Handling

```python
from src.game import ChessGame
from src.ai.stockfish import StockfishAI

game = ChessGame()

# Handle invalid moves gracefully
try:
    success = game.make_move("e2e5")  # Invalid move
    if not success:
        print("That move is not allowed")
except Exception as e:
    print(f"Error making move: {e}")

# Check AI availability
ai = StockfishAI()
if not ai.is_available():
    print("Stockfish not found, using Minimax AI instead")
    ai = MinimaxAI()
```

## Advanced Board Analysis

```python
from src.game import ChessGame
import chess

game = ChessGame()

# Analyze current position
board = game.board
print(f"Legal moves: {len(list(board.legal_moves))}")
print(f"Is check: {board.is_check()}")
print(f"Is checkmate: {board.is_checkmate()}")

# Get specific piece information
e2_square = chess.square(4, 1)  # e2
piece = game.get_piece_at(e2_square)
if piece:
    print(f"Piece at e2: {piece.symbol()}")

# Check if square is attacked
e4_square = chess.square(4, 3)  # e4
attacked = game.is_square_attacked(e4_square, chess.WHITE)
print(f"e4 attacked by white: {attacked}")
```

These examples demonstrate the main functionality of the chess game. You can mix and match these components to create custom chess applications or integrate them into larger projects.