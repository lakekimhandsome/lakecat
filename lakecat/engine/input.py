from __future__ import annotations

from dataclasses import dataclass, field
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


@dataclass(frozen=True)
class Click:
    """Screen-space mouse click. Convert to world coords via Camera."""

    screen_x: int
    screen_y: int


@dataclass
class InputFrame:
    actions: list[Action] = field(default_factory=list)
    clicks: list[Click] = field(default_factory=list)


class InputHandler:
    """Maps raw key/mouse codes to Actions and Clicks. No world or camera knowledge."""

    def poll(self, stdscr: curses.window) -> InputFrame:
        import curses

        frame = InputFrame()
        while True:
            key = stdscr.getch()
            if key == -1:
                break

            if key == curses.KEY_MOUSE:
                click = _read_click()
                if click is not None:
                    frame.clicks.append(click)
            elif key in (curses.KEY_UP, ord("w"), ord("W")):
                frame.actions.append(Action.MOVE_UP)
            elif key in (curses.KEY_DOWN, ord("s"), ord("S")):
                frame.actions.append(Action.MOVE_DOWN)
            elif key in (curses.KEY_LEFT, ord("a"), ord("A")):
                frame.actions.append(Action.MOVE_LEFT)
            elif key in (curses.KEY_RIGHT, ord("d"), ord("D")):
                frame.actions.append(Action.MOVE_RIGHT)
            elif key in (curses.KEY_ENTER, 10, 13):
                frame.actions.append(Action.CONFIRM)
            elif key in (ord("i"), ord("I")):
                frame.actions.append(Action.TOGGLE_INVENTORY)
            elif key == 27:
                frame.actions.append(Action.CANCEL)
            elif key == ord("q"):
                frame.actions.append(Action.QUIT)

        return frame


def _read_click() -> Click | None:
    import curses

    try:
        _id, mx, my, _z, bstate = curses.getmouse()
    except curses.error:
        return None

    pressed = curses.BUTTON1_PRESSED | curses.BUTTON1_CLICKED
    if bstate & pressed:
        return Click(screen_x=mx, screen_y=my)
    return None
