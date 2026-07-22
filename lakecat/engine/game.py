from __future__ import annotations

import time
from typing import TYPE_CHECKING

from lakecat.engine.debug_hud import DebugStats
from lakecat.engine.input import Action, InputHandler
from lakecat.engine.renderer import Renderer
from lakecat.world.world import World, create_demo_world

if TYPE_CHECKING:
    import curses

FPS = 60
FRAME_TIME = 1 / FPS

_MOVE_DELTA: dict[Action, tuple[int, int]] = {
    Action.MOVE_UP: (0, -1),
    Action.MOVE_DOWN: (0, 1),
    Action.MOVE_LEFT: (-1, 0),
    Action.MOVE_RIGHT: (1, 0),
}


class Game:
    """Owns the loop: input → update → render. Nothing else."""

    def __init__(self, stdscr: curses.window) -> None:
        import curses

        self._stdscr = stdscr
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)

        self._input = InputHandler()
        self._world: World = create_demo_world()
        self._renderer = Renderer(stdscr)
        self._last_frame_time = time.perf_counter()

    def run(self) -> None:
        while True:
            frame_start = time.perf_counter()
            dt = frame_start - self._last_frame_time
            self._last_frame_time = frame_start
            fps = (1.0 / dt) if dt > 0 else 0.0

            actions = self._input.poll(self._stdscr)
            if Action.QUIT in actions:
                break

            self._apply_input(actions)
            self._world.update()

            height, width = self._stdscr.getmaxyx()
            self._world.sync_camera(width, height)
            self._renderer.render(self._world, DebugStats(fps=fps))
            time.sleep(FRAME_TIME)

    def _apply_input(self, actions: list[Action]) -> None:
        for action in actions:
            delta = _MOVE_DELTA.get(action)
            if delta is not None:
                self._world.try_move_player(*delta)
