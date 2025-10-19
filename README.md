# Snake Game in Python (Turtle + Testable Engine)

A clean, extensible Snake game implemented with a **pure Python game engine** and a **Turtle graphics UI**. Built for clarity and testability with modern packaging and CI.

## ✨ Features
- Decoupled engine (`snake_game.engine`) with unit tests
- Turtle-based UI (`snake_game.turtle_ui`) with smooth animation
- Configurable board size, speed, and wrap-around mode
- PEP 621 packaging (`pyproject.toml`) with console script: `snake-game`
- CI with Ruff, Black, and Pytest

## 🚀 Quick Start
```bash
# Create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# Install (editable) with dev tools
pip install -e .[dev]

# Start the game
snake-game  # or: python -m snake_game
```

### CLI Options
```bash
snake-game --width 30 --height 20 --cell 24 --speed 100 --wrap
```
- `--width`, `--height`: board size in cells
- `--cell`: pixel size per cell in the Turtle UI
- `--speed`: tick interval in ms (lower = faster)
- `--wrap`: enable wrap-around edges (portal mode)

## 🧪 Tests
```bash
pytest -q
```

## 🧹 Lint & Format
```bash
ruff check .
black .
```

## 🏗️ Project Layout
```
src/snake_game/  # package
├── engine.py    # pure game logic (unit-testable)
├── turtle_ui.py # rendering & input via Turtle
├── config.py    # settings & defaults
└── main.py      # CLI entry point
```

## 📜 License
MIT — see [LICENSE](LICENSE).

