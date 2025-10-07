"""
Stockfish AI wrapper for chess.
"""

import subprocess
import chess
import chess.pgn
import time
import os
import platform
from typing import Optional, List, Tuple
from ..utils.constants import DIFFICULTY_LEVELS


class StockfishAI:
    """
    Wrapper for the Stockfish chess engine.
    """

    def __init__(self, stockfish_path: Optional[str] = None, difficulty: str = "medium"):
        """
        Initialize Stockfish AI.

        Args:
            stockfish_path: Path to Stockfish executable (auto-detect if None)
            difficulty: Difficulty level ('easy', 'medium', 'hard')
        """
        self.stockfish_path = stockfish_path or self._find_stockfish()
        self.difficulty = difficulty
        self.skill_level = self._get_skill_level(difficulty)
        self.process = None
        self.difficulty_settings = DIFFICULTY_LEVELS[difficulty]

        if self.stockfish_path and os.path.exists(self.stockfish_path):
            self._start_engine()

    def _find_stockfish(self) -> Optional[str]:
        """Find Stockfish executable in common locations."""
        common_paths = [
            "stockfish",
            "stockfish.exe",
            "./stockfish",
            "./stockfish.exe",
            "/usr/bin/stockfish",
            "/usr/local/bin/stockfish",
            "C:\\Program Files\\Stockfish\\stockfish.exe",
        ]

        # Check current directory and PATH
        for path in common_paths:
            if os.path.exists(path) and os.path.isfile(path):
                return path

        # Try to find in PATH
        try:
            result = subprocess.run(["which", "stockfish"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass

        return None

    def _get_skill_level(self, difficulty: str) -> int:
        """Convert difficulty to Stockfish skill level."""
        skill_map = {
            "easy": 5,
            "medium": 10,
            "hard": 20
        }
        return skill_map.get(difficulty, 10)

    def _start_engine(self):
        """Start the Stockfish engine process."""
        if not self.stockfish_path:
            return

        try:
            self.process = subprocess.Popen(
                [self.stockfish_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            # Initialize engine
            self._send_command("uci")
            self._send_command(f"setoption name Skill Level value {self.skill_level}")
            self._send_command("ucinewgame")

        except Exception as e:
            print(f"Failed to start Stockfish: {e}")
            self.process = None

    def _send_command(self, command: str) -> str:
        """Send a command to Stockfish and get response."""
        if not self.process:
            return ""

        try:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()

            # Read response
            response = ""
            while True:
                line = self.process.stdout.readline().strip()
                response += line + "\n"
                if line == "uciok" or line.startswith("bestmove"):
                    break

            return response
        except Exception:
            return ""

    def get_best_move(self, board: chess.Board) -> Optional[str]:
        """
        Get the best move from Stockfish.

        Args:
            board: Current chess board position

        Returns:
            Best move in UCI notation, or None if unavailable
        """
        if not self.process:
            return None

        try:
            # Set position
            fen = board.fen()
            self._send_command(f"position fen {fen}")

            # Set thinking time based on difficulty
            time_ms = int(self.difficulty_settings["time_limit"] * 1000)
            self._send_command(f"go movetime {time_ms}")

            # Read response
            while True:
                line = self.process.stdout.readline().strip()
                if line.startswith("bestmove"):
                    parts = line.split()
                    if len(parts) >= 2:
                        return parts[1]
                elif line.startswith("info"):
                    # Optional: parse thinking info for display
                    pass

        except Exception as e:
            print(f"Error getting move from Stockfish: {e}")
            return None

        return None

    def set_difficulty(self, difficulty: str):
        """Change the AI difficulty level."""
        if difficulty in DIFFICULTY_LEVELS:
            self.difficulty = difficulty
            self.skill_level = self._get_skill_level(difficulty)
            self.difficulty_settings = DIFFICULTY_LEVELS[difficulty]

            if self.process:
                self._send_command(f"setoption name Skill Level value {self.skill_level}")

    def set_position(self, fen: str):
        """Set the board position using FEN."""
        if self.process:
            self._send_command(f"position fen {fen}")

    def analyze_position(self, board: chess.Board) -> dict:
        """
        Get detailed analysis of current position.

        Args:
            board: Board position to analyze

        Returns:
            Dictionary with analysis information
        """
        if not self.process:
            return {}

        try:
            fen = board.fen()
            self._send_command(f"position fen {fen}")
            self._send_command("eval")

            # Read evaluation
            analysis = {}
            while True:
                line = self.process.stdout.readline().strip()
                if "Total Evaluation" in line:
                    try:
                        eval_value = float(line.split()[-1])
                        analysis['evaluation'] = eval_value
                    except:
                        pass
                elif line == "" or "Final evaluation" in line:
                    break

            return analysis
        except Exception:
            return {}

    def quit(self):
        """Quit the Stockfish engine."""
        if self.process:
            try:
                self._send_command("quit")
                self.process.terminate()
                self.process.wait()
            except Exception:
                pass
            finally:
                self.process = None

    def is_available(self) -> bool:
        """Check if Stockfish is available and running."""
        return self.process is not None and self.stockfish_path is not None

    def get_engine_info(self) -> dict:
        """Get information about the Stockfish engine."""
        info = {
            'available': self.is_available(),
            'path': self.stockfish_path,
            'difficulty': self.difficulty,
            'skill_level': self.skill_level
        }

        if self.process:
            try:
                self._send_command("uci")
                # This would need more parsing to get actual engine info
                info['uci_ok'] = True
            except Exception:
                info['uci_ok'] = False

        return info