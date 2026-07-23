from __future__ import annotations

import unicodedata
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import curses

    from lakecat.items.inventory import Inventory


def _display_width(text: str) -> int:
    """Terminal column width (emoji / wide chars count as 2)."""
    width = 0
    for ch in text:
        if unicodedata.combining(ch):
            continue
        if unicodedata.east_asian_width(ch) in ("F", "W"):
            width += 2
        else:
            width += 1
    return width


def _pad_display(text: str, width: int) -> str:
    pad = width - _display_width(text)
    if pad > 0:
        return text + (" " * pad)
    return text


class InventoryView:
    """Draws the inventory panel. Knows nothing about World / Camera / movement."""

    PANEL_WIDTH = 30

    def __init__(self, stdscr: curses.window) -> None:
        self._stdscr = stdscr

    def draw(self, inventory: Inventory, selected: int) -> None:
        height, width = self._stdscr.getmaxyx()
        lines = self._build_lines(inventory, selected)
        panel_h = len(lines)
        panel_w = min(self.PANEL_WIDTH, max(0, width - 2))
        top = max(0, (height - panel_h) // 2)
        left = max(0, (width - panel_w) // 2)

        for row_offset, line in enumerate(lines):
            row = top + row_offset
            if row >= height:
                break
            self._put(row, left, _pad_display(line, panel_w))

        self._stdscr.refresh()

    def _build_lines(self, inventory: Inventory, selected: int) -> list[str]:
        inner = self.PANEL_WIDTH - 2
        title = " Inventory "
        side = max(0, inner - _display_width(title))
        left_bar = side // 2
        right_bar = side - left_bar
        lines = [
            "╔" + ("═" * left_bar) + title + ("═" * right_bar) + "╗",
        ]

        if len(inventory) == 0:
            lines.append("║" + _pad_display(" (empty) ", inner) + "║")
        else:
            for index, slot in enumerate(inventory.slots):
                cursor = ">" if index == selected else " "
                body = f"{cursor} {slot.item.icon} {slot.item.name}"
                qty = f"×{slot.quantity}"
                gap = max(1, inner - _display_width(body) - _display_width(qty))
                row = _pad_display(body + (" " * gap) + qty, inner)
                lines.append("║" + row + "║")

        lines.append("╚" + ("═" * inner) + "╝")
        lines.append(_pad_display(" ↑↓ select   ESC close ", self.PANEL_WIDTH))
        return lines

    def _put(self, row: int, col: int, text: str) -> None:
        import curses

        try:
            self._stdscr.addstr(row, col, text)
        except curses.error:
            pass
