#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Snake Game in Python 
File: turtle_ui.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-19 
Updated: 2025-10-19 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Turtle-based graphical UI adapting the pure engine to rendering and input.

Usage: 
python -m snake_game  # or: snake-game

Notes: 
- Key bindings: Arrow keys to steer, 'R' to restart, 'Q' to quit.
- Uses world coordinates mapped to grid cells for crisp rendering.

===================================================================
"""
from __future__ import annotations

import turtle
from typing import Optional

from .config import DEFAULT_CONFIG, GameConfig
from .engine import SnakeEngine, Direction, Point


class TurtleApp:
    def __init__(self, cfg: GameConfig = DEFAULT_CONFIG) -> None:
        self.cfg = cfg
        self.engine = SnakeEngine(
            width=cfg.width, height=cfg.height, initial_len=cfg.initial_length, wrap=not cfg.border_is_deadly
        )
        self.cell = cfg.cell_px
        w_px = cfg.width * self.cell
        h_px = cfg.height * self.cell

        # Screen setup
        self.screen = turtle.Screen()
        self.screen.title("Snake Game — Turtle Edition")
        self.screen.setup(width=w_px + 40, height=h_px + 40)
        self.screen.tracer(0)
        self.screen.bgcolor("black")
        self.screen.setworldcoordinates(0, 0, cfg.width, cfg.height)

        # Drawing pen (optimized by not lifting/placing pens excessively)
        self.pen = turtle.Turtle(visible=False)
        self.pen.penup()
        self.pen.speed(0)

        # HUD
        self.hud = turtle.Turtle(visible=False)
        self.hud.penup()
        self.hud.color("white")
        self.hud.goto(1, cfg.height - 1)

        # Controls
        self._bind_keys()

    # --- Coordinate helpers -----------------------------------------------
    def _draw_cell(self, p: Point, color: str = "limegreen") -> None:
        self.pen.goto(p.x + 0.02, p.y + 0.02)
        self.pen.color(color)
        self.pen.begin_fill()
        for _ in range(4):
            self.pen.forward(0.96)
            self.pen.left(90)
        self.pen.end_fill()

    def _clear_board(self) -> None:
        self.pen.clear()

    def _draw_scene(self) -> None:
        self._clear_board()
        # Draw snake
        snake = list(self.engine.state.snake.body)
        for i, seg in enumerate(snake):
            self._draw_cell(seg, color="lime" if i == 0 else "green")
        # Draw food
        self._draw_cell(self.engine.state.food, color="red")
        # HUD
        self.hud.clear()
        self.hud.write(f"Score: {self.engine.state.score}", font=("Arial", 12, "normal"))

    # --- Input -------------------------------------------------------------
    def _bind_keys(self) -> None:
        s = self.screen
        s.listen()
        s.onkeypress(lambda: self.engine.change_direction(Direction.UP), "Up")
        s.onkeypress(lambda: self.engine.change_direction(Direction.DOWN), "Down")
        s.onkeypress(lambda: self.engine.change_direction(Direction.LEFT), "Left")
        s.onkeypress(lambda: self.engine.change_direction(Direction.RIGHT), "Right")
        s.onkeypress(self._restart, "r")
        s.onkeypress(self._quit, "q")

    # --- Loop --------------------------------------------------------------
    def _tick(self) -> None:
        state = self.engine.tick()
        self._draw_scene()
        if state.game_over:
            self._game_over_message()
        else:
            self.screen.ontimer(self._tick, self.cfg.tick_ms)

    def _game_over_message(self) -> None:
        t = turtle.Turtle(visible=False)
        t.color("white")
        t.penup()
        t.goto(self.cfg.width / 2 - 4, self.cfg.height / 2)
        t.write("GAME OVER — Press R to Restart, Q to Quit", font=("Arial", 14, "bold"))

    # --- Actions -----------------------------------------------------------
    def _restart(self) -> None:
        self.engine = SnakeEngine(
            width=self.cfg.width,
            height=self.cfg.height,
            initial_len=self.cfg.initial_length,
            wrap=not self.cfg.border_is_deadly,
        )
        self._draw_scene()

    def _quit(self) -> None:  # pragma: no cover - UI only
        turtle.bye()

    def run(self) -> None:  # pragma: no cover - UI only
        self._draw_scene()
        self.screen.ontimer(self._tick, self.cfg.tick_ms)
        turtle.mainloop()
