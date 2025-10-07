# Chess Game Project

A simple yet feature-rich chess game built in Python with Pygame, featuring both human and AI opponents. Play against a custom minimax AI or the powerful Stockfish engine with adjustable difficulty levels.

## Features

- **Interactive Chess Board**: Beautiful 8x8 board with smooth piece movement
- **Dual AI System**: Choose between educational minimax algorithm or Stockfish engine
- **Multiple Difficulty Levels**: Easy, Medium, and Hard settings for both AI types
- **Game State Tracking**: Automatic detection of check, checkmate, stalemate, and draws
- **Save/Load Games**: Save your progress and continue later
- **Multiplayer Mode**: Play against another human locally
- **Visual Feedback**: Highlight possible moves and game status
- **Sound Effects**: Optional audio feedback for moves and captures
- **Move History**: Track all moves made during the game

## Project Structure

```
Chess Game Project/
├── src/
│   ├── main.py              # Main game loop and initialization
│   ├── game.py              # Core game logic and state management
│   ├── board.py             # Pygame board rendering and interaction
│   ├── ai/
│   │   ├── minimax.py       # Custom minimax AI implementation
│   │   └── stockfish.py     # Stockfish wrapper
│   ├── ui/
│   │   ├── menu.py          # Main menu and AI selection
│   │   └── game_ui.py       # Game interface and controls
│   └── utils/
│       ├── save_load.py     # Game state persistence
│       └── constants.py     # Game constants and settings
├── assets/
│   ├── pieces/              # Chess piece images
│   └── sounds/              # Move and game sound effects
├── tests/                   # Unit tests
└── docs/                    # Additional documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/JLamour28/Chess-game-project.git
   cd Chess-game-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download chess piece assets** (Optional but recommended)
   - Place chess piece images in `assets/pieces/` directory
   - Supported formats: PNG, SVG
   - Recommended size: 64x64 pixels per piece

4. **Install Stockfish** (For Stockfish AI option)
   - Download from: https://stockfishchess.org/download/
   - Place the executable in your system PATH or in the project root

## How to Run

### Start the Game

```bash
python src/main.py
```

### Game Controls

- **Mouse**: Click and drag pieces to move them
- **Keyboard**: Use arrow keys for piece selection, Enter to confirm moves
- **Menu Navigation**: Use mouse or keyboard to navigate menus

### AI Selection

1. Launch the game
2. Choose your preferred AI opponent:
   - **Minimax AI**: Custom algorithm, educational, adjustable depth
   - **Stockfish**: World-class chess engine, very strong play

3. Select difficulty level:
   - **Easy**: Faster moves, suitable for beginners
   - **Medium**: Balanced difficulty and response time
   - **Hard**: Deep analysis, challenging gameplay

## Usage Examples

### Basic Gameplay

```python
from src.game import ChessGame
from src.ai.minimax import MinimaxAI

# Initialize game
game = ChessGame()

# Create AI opponent
ai = MinimaxAI(difficulty="medium")

# Make moves
game.make_move("e2e4")  # Human move
ai_move = ai.get_best_move(game.board)  # AI move
game.make_move(ai_move)
```

### Save and Load Games

```python
from src.utils.save_load import save_game, load_game

# Save current game
save_game(game, "my_game.json")

# Load saved game
loaded_game = load_game("my_game.json")
```

## Development

### Running Tests

```bash
python -m unittest discover tests/
```

### Code Structure

The project follows a modular architecture:

- **`game.py`**: Core game logic and chess rules
- **`board.py`**: Visual board representation and rendering
- **`ai/`**: AI implementations (minimax and Stockfish)
- **`ui/`**: User interface components
- **`utils/`**: Helper functions and constants

### Adding New Features

1. **New AI Algorithm**: Implement in `src/ai/` following the existing interface
2. **UI Enhancements**: Modify `src/ui/game_ui.py` for visual changes
3. **Game Rules**: Extend `src/game.py` for rule modifications

## Configuration

Game settings can be modified in `src/utils/constants.py`:

```python
# Board settings
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8

# AI settings
DEFAULT_DIFFICULTY = "medium"
MAX_SEARCH_DEPTH = 4

# Game settings
ENABLE_SOUNDS = True
ANIMATION_SPEED = 0.1
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Performance Tips

- For faster AI moves on Hard difficulty, reduce `MAX_SEARCH_DEPTH` in constants
- Disable sound effects in `constants.py` for better performance
- Use piece images instead of Unicode characters for smoother rendering

## Troubleshooting

### Common Issues

1. **Pygame window doesn't open**: Ensure your system supports GUI applications
2. **Stockfish not found**: Add Stockfish to your system PATH or place in project root
3. **Import errors**: Run `pip install -r requirements.txt` to install dependencies

### Getting Help

- Check the `docs/` directory for detailed documentation
- Open an issue on GitHub for bugs or feature requests
- Review the example code in `docs/examples/`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [python-chess](https://python-chess.readthedocs.io/) for chess logic
- [Pygame](https://www.pygame.org/) for graphics and user interface
- [Stockfish](https://stockfishchess.org/) for world-class AI opponent