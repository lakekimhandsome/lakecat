"""Load large ASCII art assets from files beside this package."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=None)
def load_ascii_art(filename: str = "ascii-art.txt") -> tuple[str, ...]:
    path = Path(__file__).with_name(filename)
    return tuple(path.read_text(encoding="utf-8").splitlines())
