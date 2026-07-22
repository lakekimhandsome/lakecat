from __future__ import annotations

from lakecat.world.map import Map


def rects_overlap(
    ax: int,
    ay: int,
    aw: int,
    ah: int,
    bx: int,
    by: int,
    bw: int,
    bh: int,
) -> bool:
    """Axis-aligned bounding box overlap in world space."""
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def can_move_to(
    game_map: Map,
    x: int,
    y: int,
    width: int,
    height: int,
) -> bool:
    """True if a rectangle at (x, y) does not hit any solid object on the map."""
    for obj in game_map.objects:
        if not obj.solid:
            continue
        if rects_overlap(
            x,
            y,
            width,
            height,
            obj.world_x,
            obj.world_y,
            obj.width,
            obj.height,
        ):
            return False
    return True
