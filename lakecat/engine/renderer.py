from __future__ import annotations

from typing import TYPE_CHECKING

from lakecat.engine.debug_hud import DebugHud, DebugStats
from lakecat.entities.player import Player
from lakecat.world.objects import GameObject

if TYPE_CHECKING:
    import curses

    from lakecat.engine.camera import Camera
    from lakecat.world.world import World


class Renderer:
    """Only place that turns world positions into drawn cells."""

    def __init__(self, stdscr: curses.window) -> None:
        self._stdscr = stdscr
        self._debug_hud = DebugHud()

    def render(
        self,
        world: World,
        stats: DebugStats | None = None,
        *,
        overlay: list[str] | tuple[str, ...] | None = None,
    ) -> None:
        self._stdscr.clear()

        if overlay is not None:
            self._draw_screen_overlay(overlay)
            self._stdscr.refresh()
            return

        camera = world.camera
        player = world.player

        # Decorations (flowers, etc.) never cover the player.
        for obj in world.map.objects:
            if obj.occludes:
                continue
            sx, sy = camera.world_to_screen(obj.world_x, obj.world_y)
            self._draw_sprite(obj.sprite, sx, sy, camera.height, camera.width)

        # Occluders + player: lower foot-Y draws later (in front).
        draw_list: list[tuple[int, int, str, GameObject | Player]] = []
        for index, obj in enumerate(world.map.objects):
            if not obj.occludes:
                continue
            draw_list.append((obj.sort_y, index, "object", obj))
        player_sort_y = player.position.y + player.height - 1
        draw_list.append((player_sort_y, len(draw_list), "player", player))
        draw_list.sort(key=lambda item: (item[0], item[1]))

        player_drawn = False
        for _, _, kind, item in draw_list:
            if kind == "player":
                assert isinstance(item, Player)
                sx, sy = camera.world_to_screen(item.position.x, item.position.y)
                self._draw_glyph(item.glyph, sx, sy, camera.height, camera.width)
                player_drawn = True
                continue

            assert isinstance(item, GameObject)
            if player_drawn and _covers_player(item, player):
                # Erase the full 2-cell cat footprint so a wide emoji is not left half-drawn.
                self._clear_player_footprint(player, camera)
            sx, sy = camera.world_to_screen(item.world_x, item.world_y)
            self._draw_sprite(item.sprite, sx, sy, camera.height, camera.width)

        self._draw_debug_hud(world, stats or DebugStats())
        self._stdscr.refresh()

    def _clear_player_footprint(self, player: Player, camera: Camera) -> None:
        """Blank every cell the player occupies (width accounts for 2-cell horizontal span)."""
        for row_offset in range(player.height):
            for col_offset in range(player.width):
                sx, sy = camera.world_to_screen(
                    player.position.x + col_offset,
                    player.position.y + row_offset,
                )
                if 0 <= sy < camera.height and 0 <= sx < camera.width:
                    self._put(sy, sx, " ")

    def _draw_screen_overlay(self, lines: list[str] | tuple[str, ...]) -> None:
        """Full-screen art. Screen coordinates only — camera never involved."""
        height, width = self._stdscr.getmaxyx()
        for row, line in enumerate(lines):
            if row >= height:
                break
            if width <= 0:
                break
            self._put(row, 0, line[: width - 1] if width > 1 else "")

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


def _covers_player(obj: GameObject, player: Player) -> bool:
    """True if the object's silhouette (including hollow interiors) overlaps the player."""
    for row_offset in range(player.height):
        for col_offset in range(player.width):
            if obj.covers_cell(
                player.position.x + col_offset,
                player.position.y + row_offset,
            ):
                return True
    return False
