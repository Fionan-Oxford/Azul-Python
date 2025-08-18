# Azul Python

A Python implementation of the board game Azul.  
This project provides both a backend engine for game logic and a simple Tkinter GUI for playing.

## Features
- Full two-player Azul ruleset (with a few simplifications noted in the code).
- Backend API (`Game` class) that handles:
  - Factory offers
  - Pattern lines
  - Floor penalties
  - Wall tiling
  - Automatic state progression and scoring
- GUI frontend (`AzulGUI.py`) built with Tkinter.
- Modular design: factories, walls, floors, tiles, and states are implemented as separate classes.

## Getting Started

### Requirements
- Python 3.10+
- Tkinter (usually bundled with Python)

### Run the game
```bash
python AzulGUI.py
```

### Use the backend in your own project
```python
from azul_backend.game import Game

game = Game()
print(game.show_game_state())
```

## Project Structure
```
azul_backend/
├── factory.py        # Manages tile factories
├── floor.py          # Player floor & penalties
├── game.py           # Main game facade
├── patternlines.py   # Pattern lines logic
├── states.py         # Game states (enum)
├── tilebag.py        # Tile bag mechanics
├── tiles.py          # Tile definitions
├── wall.py           # Player wall & scoring
AzulGUI.py            # Tkinter GUI frontend
```

## Development

Clone the repo:
```bash
git clone https://github.com/yourusername/azul-python.git
cd azul-python
```

Run the GUI or explore the backend via an interactive shell or Jupyter notebook.  
Unit tests can be added under `tests/`.

## Contributing

Contributions are welcome. Some ideas:
- Add more unit tests and improve test coverage.
- Enhance the GUI (better layout, animations, themes).
- Support more than 2 players.
- Implement full Azul scoring (rows, columns, completed sets).
- Build a web or mobile frontend.

To contribute:
1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/my-change`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to your fork and open a pull request.

## License
BSD 2-Clause License (see [LICENSE.md](LICENSE.md) for details)
