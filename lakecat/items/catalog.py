from __future__ import annotations

from lakecat.items.item import Item

WOOD = Item(id="wood", name="Wood", icon="🪵", max_stack=99)
STONE = Item(id="stone", name="Stone", icon="🪨", max_stack=99)
FISH = Item(id="fish", name="Fish", icon="🐟", max_stack=99)

ITEMS: dict[str, Item] = {
    WOOD.id: WOOD,
    STONE.id: STONE,
    FISH.id: FISH,
}


def get_item(item_id: str) -> Item:
    return ITEMS[item_id]
