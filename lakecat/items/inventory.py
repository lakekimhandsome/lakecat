from __future__ import annotations

from dataclasses import dataclass, field

from lakecat.items.item import Item


@dataclass
class InventorySlot:
    """One stack in the bag. Future: equip/trade operate on slots."""

    item: Item
    quantity: int

    def space_left(self) -> int:
        return max(0, self.item.max_stack - self.quantity)


@dataclass
class Inventory:
    """Stacked item storage. UI and world systems call this; it draws nothing."""

    capacity: int = 20
    _slots: list[InventorySlot] = field(default_factory=list)

    @property
    def slots(self) -> list[InventorySlot]:
        return self._slots

    def __len__(self) -> int:
        return len(self._slots)

    def get(self, index: int) -> InventorySlot | None:
        if 0 <= index < len(self._slots):
            return self._slots[index]
        return None

    def count(self, item_id: str) -> int:
        return sum(slot.quantity for slot in self._slots if slot.item.id == item_id)

    def add(self, item: Item, amount: int = 1) -> int:
        """Add items, stacking into existing slots. Returns leftover that did not fit."""
        if amount <= 0:
            return 0
        remaining = amount

        for slot in self._slots:
            if slot.item.id != item.id:
                continue
            take = min(remaining, slot.space_left())
            if take <= 0:
                continue
            slot.quantity += take
            remaining -= take
            if remaining == 0:
                return 0

        while remaining > 0 and len(self._slots) < self.capacity:
            take = min(remaining, item.max_stack)
            self._slots.append(InventorySlot(item=item, quantity=take))
            remaining -= take

        return remaining

    def remove(self, item_id: str, amount: int = 1) -> bool:
        """Remove up to amount of item_id. False if not enough."""
        if amount <= 0:
            return True
        if self.count(item_id) < amount:
            return False

        remaining = amount
        for slot in list(self._slots):
            if slot.item.id != item_id:
                continue
            take = min(remaining, slot.quantity)
            slot.quantity -= take
            remaining -= take
            if slot.quantity <= 0:
                self._slots.remove(slot)
            if remaining == 0:
                break
        return True

    def remove_at(self, index: int, amount: int = 1) -> Item | None:
        """Remove from a specific slot (drop / use / trade). Returns the item type."""
        slot = self.get(index)
        if slot is None or amount <= 0 or amount > slot.quantity:
            return None
        item = slot.item
        slot.quantity -= amount
        if slot.quantity <= 0:
            self._slots.pop(index)
        return item
