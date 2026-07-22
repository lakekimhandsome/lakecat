from __future__ import annotations

from typing import TYPE_CHECKING

from lakecat.engine.debug_hud import DebugHud, DebugStats

if TYPE_CHECKING:
    import curses

    from lakecat.world.world import World


class Renderer:
    """Only place that turns world positions into drawn cells."""

    def __init__(self, stdscr: curses.window) -> None:
        self._stdscr = stdscr
        self._debug_hud = DebugHud()

    def render(self, world: World, stats: DebugStats | None = None) -> None:
        camera = world.camera
        self._stdscr.clear()

        for obj in world.map.objects:
            sx, sy = camera.world_to_screen(obj.world_x, obj.world_y)
            self._draw_sprite(obj.sprite, sx, sy, camera.height, camera.width)

        player = world.player
        sx, sy = camera.world_to_screen(player.position.x, player.position.y)
        self._draw_glyph(player.glyph, sx, sy, camera.height, camera.width)

        self._draw_debug_hud(world, stats or DebugStats())
        self._stdscr.refresh()

    def _draw_debug_hud(self, world: World, stats: DebugStats) -> None:
        """Screen-fixed overlay. Never uses the camera."""
        height, width = self._stdscr.getmaxyx()
        for row, line in enumerate(self._debug_hud.lines(world, stats)):
            if row >= height:
                break
            self._put(row, 0, line[:width])

    def _draw_sprite(
        self,
        sprite: list[str],
        screen_x: int,
        screen_y: int,
        height: int,
        width: int,
    ) -> None:
        for row_offset, line in enumerate(sprite):
            row = screen_y + row_offset
            if row < 0 or row >= height:
                continue
            for col_offset, ch in enumerate(line):
                if ch == " ":
                    continue
                col = screen_x + col_offset
                if 0 <= col < width:
                    self._put(row, col, ch)

    def _draw_glyph(
        self,
        glyph: str,
        screen_x: int,
        screen_y: int,
        height: int,
        width: int,
    ) -> None:
        if 0 <= screen_y < height and 0 <= screen_x < width:
            self._put(screen_y, screen_x, glyph)

    def _put(self, row: int, col: int, text: str) -> None:
        import curses

        try:
            self._stdscr.addstr(row, col, text)
        except curses.error:
            # curses can raise near the bottom-right corner; skip safely
            pass
