#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Snake Game in Python 
File: engine.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-19 
Updated: 2025-10-19 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Pure game logic and state machine for Snake. UI-agnostic and unit-testable.

Usage: 
python -c "from snake_game.engine import SnakeEngine; e=SnakeEngine(10,10); print(e.state)"

Notes: 
- Provides Direction, Point, Snake, GameState, and SnakeEngine classes.
- Handles movement, growth, food placement, self/wall collisions, and optional wrapping.

===================================================================
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, List, Tuple
import random


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    @staticmethod
    def opposite(a: "Direction", b: "Direction") -> bool:
        return (a, b) in {
            (Direction.UP, Direction.DOWN),
            (Direction.DOWN, Direction.UP),
            (Direction.LEFT, Direction.RIGHT),
            (Direction.RIGHT, Direction.LEFT),
        }


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Snake:
    body: List[Point]
    direction: Direction
    _grow: int = 0

    @property
    def head(self) -> Point:
        return self.body[0]

    def set_direction(self, new_dir: Direction) -> None:
        # Prevent reversing directly into itself
        if not Direction.opposite(self.direction, new_dir):
            self.direction = new_dir

    def step(self, next_head: Point) -> None:
        self.body.insert(0, next_head)
        if self._grow > 0:
            self._grow -= 1
        else:
            self.body.pop()

    def grow(self, n: int = 1) -> None:
        self._grow += max(1, n)

    def occupies(self, p: Point) -> bool:
        return p in self.body


@dataclass
class GameState:
    width: int
    height: int
    snake: Snake
    food: Point
    score: int = 0
    game_over: bool = False
    wrap: bool = False  # if True, edges wrap instead of collide


class SnakeEngine:
    """Encapsulates the game logic and state transitions."""

    def __init__(self, width: int, height: int, initial_len: int = 3, wrap: bool = False) -> None:
        assert width > 4 and height > 4, "Board too small"
        self.rng = random.Random()
        # Initialize snake centered and horizontal to the right
        cx, cy = width // 2, height // 2
        body = [Point(cx - i, cy) for i in range(initial_len)]
        snake = Snake(body=body, direction=Direction.RIGHT)
        self.state = GameState(
            width=width,
            height=height,
            snake=snake,
            food=Point(0, 0),
            score=0,
            game_over=False,
            wrap=wrap,
        )
        self._place_food()

    # --- Utility -----------------------------------------------------------
    def _random_empty_cell(self) -> Point:
        while True:
            p = Point(self.rng.randrange(self.state.width), self.rng.randrange(self.state.height))
            if not self.state.snake.occupies(p):
                return p

    def _place_food(self) -> None:
        self.state.food = self._random_empty_cell()

    # --- Mechanics ---------------------------------------------------------
    def change_direction(self, new_dir: Direction) -> None:
        self.state.snake.set_direction(new_dir)

    def _next_head(self) -> Point:
        head = self.state.snake.head
        dx, dy = {
            Direction.UP: (0, 1),
            Direction.DOWN: (0, -1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
        }[self.state.snake.direction]
        nx, ny = head.x + dx, head.y + dy
        if self.state.wrap:
            nx %= self.state.width
            ny %= self.state.height
        return Point(nx, ny)

    def _hits_wall(self, p: Point) -> bool:
        return not (0 <= p.x < self.state.width and 0 <= p.y < self.state.height)

    def _hits_self(self, p: Point) -> bool:
        # Exclude the tail if it will move this tick (unless growing)
        body = self.state.snake.body
        will_grow = self.state.snake._grow > 0
        check_body = body if will_grow else body[:-1]
        return p in check_body

    def tick(self) -> GameState:
        if self.state.game_over:
            return self.state

        next_head = self._next_head()

        # Collisions
        if (not self.state.wrap and self._hits_wall(next_head)) or self._hits_self(next_head):
            self.state.game_over = True
            return self.state

        # Movement
        self.state.snake.step(next_head)

        # Eating
        if next_head == self.state.food:
            self.state.snake.grow(1)
            self.state.score += 1
            self._place_food()

        return self.state

    # --- Debug / helpers ---------------------------------------------------
    def snake_cells(self) -> Iterable[Tuple[int, int]]:
        return ((p.x, p.y) for p in self.state.snake.body)
