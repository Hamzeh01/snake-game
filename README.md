# Python Snake Game

A modern, feature-rich implementation of the classic Snake game using Python and Pygame.

## Features

- Multiple gameplay modes:
  - Classic Mode: Traditional snake game
  - Time Attack Mode: Race against the clock
  - Challenge Mode: Obstacles and special items
- Customizable settings:
  - Snake color and appearance
  - Game speed
  - Food types and appearance
- Resizable game window
- High score tracking
- User-friendly controls

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/snake-game.git
cd snake-game
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the game:
```bash
python -m snake_game
```

### Controls
- Arrow keys or WASD: Control snake movement
- P: Pause game
- ESC: Exit game
- Space: Start/Restart game
- M: Toggle game mode

## Project Structure
```
snake_game/
├── snake_game/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game.py        # Main game logic
│   │   ├── snake.py       # Snake class
│   │   └── food.py        # Food class
│   ├── modes/
│   │   ├── __init__.py
│   │   ├── classic.py     # Classic game mode
│   │   ├── timed.py       # Time attack mode
│   │   └── challenge.py   # Challenge mode
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── colors.py      # Color definitions
│   │   └── renderer.py    # Game rendering
│   └── utils/
│       ├── __init__.py
│       ├── config.py      # Game configuration
│       └── settings.py    # User settings
└── tests/
    ├── __init__.py
    ├── test_game.py
    ├── test_snake.py
    └── test_food.py
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

## Requirements

- Python 3.8+
- Pygame 2.0+
- Other dependencies listed in requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.
