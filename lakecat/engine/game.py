from __future__ import annotations

import time
from typing import TYPE_CHECKING

from lakecat.assets.art import load_ascii_art
from lakecat.engine.debug_hud import DebugStats
from lakecat.engine.input import Action, InputHandler
from lakecat.engine.renderer import Renderer
from lakecat.ui.inventory_view import InventoryView
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
        curses.set_escdelay(25)

        self._input = InputHandler()
        self._world: World = create_demo_world()
        self._renderer = Renderer(stdscr)
        self._inventory_view = InventoryView(stdscr)
        self._last_frame_time = time.perf_counter()
        self._show_ascii_art = False
        self._ascii_art = load_ascii_art()
        self._inventory_open = False
        self._inventory_cursor = 0

    def run(self) -> None:
        while True:
            frame_start = time.perf_counter()
            dt = frame_start - self._last_frame_time
            self._last_frame_time = frame_start
            fps = (1.0 / dt) if dt > 0 else 0.0

            actions = self._input.poll(self._stdscr)
            if Action.QUIT in actions:
                break

            self._handle_actions(actions)

            if not self._show_ascii_art and not self._inventory_open:
                self._world.update()

            height, width = self._stdscr.getmaxyx()
            self._world.sync_camera(width, height)

            if self._show_ascii_art:
                self._renderer.render(
                    self._world,
                    DebugStats(fps=fps),
                    overlay=self._ascii_art,
                )
            else:
                self._renderer.render(self._world, DebugStats(fps=fps))
                if self._inventory_open:
                    self._inventory_view.draw(
                        self._world.player.inventory,
                        self._inventory_cursor,
                    )
            time.sleep(FRAME_TIME)

    def _handle_actions(self, actions: list[Action]) -> None:
        if self._inventory_open:
            self._handle_inventory_actions(actions)
            return

        if Action.TOGGLE_INVENTORY in actions and not self._show_ascii_art:
            self._open_inventory()
            return

        if Action.CONFIRM in actions:
            self._show_ascii_art = not self._show_ascii_art

        if not self._show_ascii_art:
            self._apply_movement(actions)

    def _handle_inventory_actions(self, actions: list[Action]) -> None:
        if Action.CANCEL in actions or Action.TOGGLE_INVENTORY in actions:
            self._inventory_open = False
            return

        size = len(self._world.player.inventory)
        if size == 0:
            return

        for action in actions:
            if action in (Action.MOVE_UP, Action.MOVE_LEFT):
                self._inventory_cursor = (self._inventory_cursor - 1) % size
            elif action in (Action.MOVE_DOWN, Action.MOVE_RIGHT):
                self._inventory_cursor = (self._inventory_cursor + 1) % size
            # CONFIRM reserved for future use / equip / drop menu

    def _open_inventory(self) -> None:
        self._inventory_open = True
        size = len(self._world.player.inventory)
        if size == 0:
            self._inventory_cursor = 0
        else:
            self._inventory_cursor = min(self._inventory_cursor, size - 1)

    def _apply_movement(self, actions: list[Action]) -> None:
        for action in actions:
            delta = _MOVE_DELTA.get(action)
            if delta is not None:
                self._world.try_move_player(*delta)
