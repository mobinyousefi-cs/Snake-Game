#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Snake Game in Python 
File: __init__.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-19 
Updated: 2025-10-19 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Package initializer exposing package version metadata.

Usage: 
python -m snake_game

Notes: 
- Uses importlib.metadata; falls back to "0.0.0" during local dev if distribution metadata is unavailable.

===================================================================
"""
from importlib.metadata import version, PackageNotFoundError

try:  # pragma: no cover - metadata
    __version__ = version("snake-game")
except PackageNotFoundError:  # pragma: no cover - during local dev
    __version__ = "0.0.0"

__all__ = ["__version__"]
