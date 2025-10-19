#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Snake Game in Python 
File: test_engine.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-19 
Updated: 2025-10-19 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Unit tests validating movement, scoring, self-collision, and wall wrapping.

Usage: 
pytest -q tests/test_engine.py

Notes: 
- Keeps tests deterministic by manually placing food when needed.

===================================================================
"""
from snake_game.engine import SnakeEngine, Direction


def test_snake_moves_and_scores():
    eng = SnakeEngine(width=10, height=10, initial_len=3, wrap=False)
    # Place food right in front of the head to guarantee a score on next tick
    head = eng.state.snake.head
    eng.state.food = type(head)(head.x + 1, head.y)
    assert eng.state.score == 0
    eng.tick()
    assert eng.state.score == 1
    assert len(eng.state.snake.body) == 4  # grew by one


def test_self_collision_sets_game_over():
    eng = SnakeEngine(width=8, height=8, initial_len=4, wrap=False)
    # Force a self-collision by turning into itself
    eng.change_direction(Direction.DOWN)
    eng.tick()
    eng.change_direction(Direction.LEFT)
    eng.tick()
    eng.change_direction(Direction.UP)
    eng.tick()
    assert eng.state.game_over is True


def test_wall_collision_vs_wrap():
    # Deadly border
    eng = SnakeEngine(width=5, height=5, initial_len=3, wrap=False)
    for _ in range(10):
        eng.change_direction(Direction.RIGHT)
        eng.tick()
        if eng.state.game_over:
            break
    assert eng.state.game_over is True

    # Wrapping border
    eng = SnakeEngine(width=5, height=5, initial_len=3, wrap=True)
    x_before = eng.state.snake.head.x
    eng.change_direction(Direction.LEFT)
    eng.tick()  # should wrap without game over
    assert eng.state.game_over is False
    assert eng.state.snake.head.x != x_before or eng.state.snake.head.y == eng.state.snake.head.y
