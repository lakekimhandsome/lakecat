"""Entry point. Keep this file thin — all logic lives in the engine."""

import curses

from lakecat.engine.game import Game


def run() -> None:
    curses.wrapper(lambda stdscr: Game(stdscr).run())


if __name__ == "__main__":
    run()
