#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Snake Game in Python 
File: main.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-19 
Updated: 2025-10-19 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
CLI entry point for launching the Turtle-based Snake game.

Usage: 
python -m snake_game --width 30 --height 20 --cell 24 --speed 100 --wrap

Notes: 
- Exposes CLI flags for board size, cell size, speed (ms), and wrapping behavior.

===================================================================
"""
from __future__ import annotations

import argparse

from .config import GameConfig
from .turtle_ui import TurtleApp


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Snake Game in Python (Turtle UI)")
    p.add_argument("--width", type=int, default=GameConfig.width, help="Board width in cells (default: 24)")
    p.add_argument("--height", type=int, default=GameConfig.height, help="Board height in cells (default: 18)")
    p.add_argument("--cell", type=int, default=GameConfig.cell_px, help="Cell size in pixels (default: 24)")
    p.add_argument(
        "--wrap",
        action="store_true",
        help="Wrap around edges (Portal mode). Default is deadly borders.",
    )
    p.add_argument("--speed", type=int, default=GameConfig.tick_ms, help="Tick in ms (lower=faster). Default: 120")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = GameConfig(
        width=args.width,
        height=args.height,
        cell_px=args.cell,
        tick_ms=args.speed,
        border_is_deadly=not args.wrap,
    )
    TurtleApp(cfg).run()


if __name__ == "__main__":  # pragma: no cover
    main()
