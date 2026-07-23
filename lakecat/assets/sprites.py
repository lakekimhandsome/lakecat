"""ASCII sprites. Keep presentation data out of game logic."""

TREE: list[str] = [
    "   /\\   ",
    "  /  \\  ",
    " /    \\ ",
    "/______\\",
    "   ||   ",
]
# Only the trunk "||" blocks movement: (offset_x, offset_y, width, height).
TREE_HITBOX: tuple[int, int, int, int] = (3, 4, 2, 1)

FLOWER: list[str] = [
    " @ ",
    "\\|/",
    " | ",
]

PLAYER_GLYPH = "🐈"
