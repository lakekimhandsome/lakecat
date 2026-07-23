from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import curses


class Action(Enum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    CONFIRM = auto()
    QUIT = auto()
    TOGGLE_INVENTORY = auto()
    CANCEL = auto()


class InputHandler:
    """Maps raw key codes to game Actions. No world or camera knowledge."""

    def poll(self, stdscr: curses.window) -> list[Action]:
        import curses

        actions: list[Action] = []
        while True:
            key = stdscr.getch()
            if key == -1:
                break

            if key in (curses.KEY_UP, ord("w"), ord("W")):
                actions.append(Action.MOVE_UP)
            elif key in (curses.KEY_DOWN, ord("s"), ord("S")):
                actions.append(Action.MOVE_DOWN)
            elif key in (curses.KEY_LEFT, ord("a"), ord("A")):
                actions.append(Action.MOVE_LEFT)
            elif key in (curses.KEY_RIGHT, ord("d"), ord("D")):
                actions.append(Action.MOVE_RIGHT)
            elif key in (curses.KEY_ENTER, 10, 13):
                actions.append(Action.CONFIRM)
            elif key in (ord("i"), ord("I")):
                actions.append(Action.TOGGLE_INVENTORY)
            elif key == 27:
                actions.append(Action.CANCEL)
            elif key == ord("q"):
                actions.append(Action.QUIT)

        return actions
