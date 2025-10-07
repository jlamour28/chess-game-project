"""
Save and load game functionality.
"""

import json
import os
from typing import Dict, Any
from ..game import ChessGame


def save_game(game: ChessGame, filename: str) -> bool:
    """
    Save the current game state to a file.

    Args:
        game: ChessGame instance to save
        filename: Path to save file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        game_data = {
            'fen': game.get_board_fen(),
            'move_history': game.move_history,
            'current_player': game.current_player,
            'game_state': game.game_state
        }

        with open(filename, 'w') as f:
            json.dump(game_data, f, indent=2)
        return True
    except Exception:
        return False


def load_game(filename: str) -> ChessGame:
    """
    Load a game state from a file.

    Args:
        filename: Path to save file

    Returns:
        ChessGame: Loaded game instance, or new game if loading fails
    """
    game = ChessGame()

    try:
        if not os.path.exists(filename):
            return game

        with open(filename, 'r') as f:
            game_data = json.load(f)

        # Load FEN position
        if 'fen' in game_data:
            game.load_from_fen(game_data['fen'])

        # Restore other game data
        if 'move_history' in game_data:
            game.move_history = game_data['move_history']

        if 'current_player' in game_data:
            game.current_player = game_data['current_player']

        if 'game_state' in game_data:
            game.game_state = game_data['game_state']

        return game
    except Exception:
        return game


def get_saved_games(directory: str = "game_saves") -> Dict[str, Dict[str, Any]]:
    """
    Get a list of all saved games in a directory.

    Args:
        directory: Directory to search for saved games

    Returns:
        Dict mapping filename to game metadata
    """
    saved_games = {}

    if not os.path.exists(directory):
        os.makedirs(directory)
        return saved_games

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as f:
                    game_data = json.load(f)

                saved_games[filename] = {
                    'filepath': filepath,
                    'fen': game_data.get('fen', ''),
                    'move_count': len(game_data.get('move_history', [])),
                    'game_state': game_data.get('game_state', 'unknown')
                }
            except Exception:
                continue

    return saved_games


def delete_saved_game(filename: str, directory: str = "game_saves") -> bool:
    """
    Delete a saved game file.

    Args:
        filename: Name of the save file to delete
        directory: Directory containing the save file

    Returns:
        bool: True if successful, False otherwise
    """
    filepath = os.path.join(directory, filename)

    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception:
        return False