#!/usr/bin/env python3
"""
Basic test script to verify the chess game functionality.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from game import ChessGame
        from ai.minimax import MinimaxAI
        from ai.stockfish import StockfishAI
        from utils.save_load import save_game, load_game
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_game_creation():
    """Test creating a new game."""
    try:
        from game import ChessGame

        game = ChessGame()
        print(f"✓ Game created successfully")
        print(f"  - Current player: {'White' if game.current_player else 'Black'}")
        print(f"  - Game state: {game.game_state}")
        print(f"  - Move history length: {len(game.move_history)}")
        return True
    except Exception as e:
        print(f"✗ Game creation failed: {e}")
        return False

def test_basic_moves():
    """Test making some basic moves."""
    try:
        from game import ChessGame

        game = ChessGame()

        # Test opening moves
        moves = ["e2e4", "e7e5", "g1f3", "b8c6"]

        for i, move in enumerate(moves):
            success = game.make_move(move)
            if not success:
                print(f"✗ Move {i+1} failed: {move}")
                return False

        print(f"✓ Successfully made {len(moves)} moves")
        print(f"  - Current player: {'White' if game.current_player else 'Black'}")
        print(f"  - Move history: {game.move_history}")
        return True
    except Exception as e:
        print(f"✗ Basic moves test failed: {e}")
        return False

def test_ai_minimax():
    """Test minimax AI."""
    try:
        from game import ChessGame
        from ai.minimax import MinimaxAI

        game = ChessGame()
        ai = MinimaxAI(difficulty="easy")

        # Get AI move
        move = ai.get_best_move(game.board)

        if move:
            print(f"✓ Minimax AI suggested move: {move}")

            # Try to make the move
            success = game.make_move(move)
            if success:
                print("✓ AI move executed successfully")
                return True
            else:
                print("✗ Could not execute AI move")
                return False
        else:
            print("✗ AI returned no move")
            return False
    except Exception as e:
        print(f"✗ Minimax AI test failed: {e}")
        return False

def test_ai_stockfish():
    """Test Stockfish AI."""
    try:
        from game import ChessGame
        from ai.stockfish import StockfishAI

        game = ChessGame()
        ai = StockfishAI(difficulty="easy")

        if ai.is_available():
            move = ai.get_best_move(game.board)

            if move:
                print(f"✓ Stockfish AI suggested move: {move}")

                # Try to make the move
                success = game.make_move(move)
                if success:
                    print("✓ Stockfish move executed successfully")
                    return True
                else:
                    print("✗ Could not execute Stockfish move")
                    return False
            else:
                print("✗ Stockfish returned no move")
                return False
        else:
            print("⚠ Stockfish not available, skipping test")
            return True
    except Exception as e:
        print(f"✗ Stockfish AI test failed: {e}")
        return False

def test_save_load():
    """Test save/load functionality."""
    try:
        from game import ChessGame
        from utils.save_load import save_game, load_game

        # Create and modify game
        game = ChessGame()
        game.make_move("e2e4")
        game.make_move("e7e5")

        # Save game
        filename = "test_save.json"
        success = save_game(game, filename)

        if success:
            print("✓ Game saved successfully")
        else:
            print("✗ Failed to save game")
            return False

        # Load game
        loaded_game = load_game(filename)

        if loaded_game:
            print("✓ Game loaded successfully")
            print(f"  - Original moves: {game.move_history}")
            print(f"  - Loaded moves: {loaded_game.move_history}")

            if game.move_history == loaded_game.move_history:
                print("✓ Save/load data integrity verified")
                # Cleanup
                if os.path.exists(filename):
                    os.remove(filename)
                return True
            else:
                print("✗ Save/load data mismatch")
                return False
        else:
            print("✗ Failed to load game")
            return False
    except Exception as e:
        print(f"✗ Save/load test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Chess Game - Basic Functionality Test")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("Game Creation", test_game_creation),
        ("Basic Moves", test_basic_moves),
        ("Minimax AI", test_ai_minimax),
        ("Stockfish AI", test_ai_stockfish),
        ("Save/Load", test_save_load),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1

    print(f"\n{'=' * 50}")
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! The chess game is ready to use.")
        print("\nTo run the full game:")
        print("  python src/main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nMake sure you have installed the required dependencies:")
        print("  pip install -r requirements.txt")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)