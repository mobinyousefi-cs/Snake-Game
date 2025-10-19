#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Snake Game in Python 
File: config.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-19 
Updated: 2025-10-19 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Configuration dataclass and defaults for the Snake game.

Usage: 
python -c "from snake_game.config import DEFAULT_CONFIG; print(DEFAULT_CONFIG)"

Notes: 
- Tunable parameters: board size, cell pixels, initial length, tick speed, and border behavior.

===================================================================
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    width: int = 24   # grid cells
    height: int = 18  # grid cells
    cell_px: int = 24 # pixel size per cell in Turtle UI
    initial_length: int = 3
    tick_ms: int = 120  # engine tick in milliseconds (UI)
    border_is_deadly: bool = True  # if False, snake wraps around


DEFAULT_CONFIG = GameConfig()
