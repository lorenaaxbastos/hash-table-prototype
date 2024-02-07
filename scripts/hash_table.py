from typing import NamedTuple, Any

class Pair(NamedTuple):
    key: Any
    value: Any

class HashTable:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity should be a positive number and greater than zero.")
        self._slots = capacity * [None]

    def __len__(self):
        return len(self.items)

    def __setitem__(self, key, value):
        self._slots[self._index(key)] = Pair(key, value)

    def __getitem__(self, key):
        _slots = self._slots[self._index(key)]
        if _slots is None:
            raise KeyError(key)
        return _slots.value

    def __delitem__(self, key):
        if key in self:
            self._slots[self._index(key)] = None
        else:
            raise KeyError(key)

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __iter__(self):
        yield from self.keys

    def __repr__(self):
        items = []
        for key, value in self.items:
            items.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(items) + "}"

    def _index(self, key):
        return hash(key) % self.capacity

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    @property
    def items(self):
        return {items for items in self._slots if items}

    @property
    def values(self):
        return [items.value for items in self.items]

    @property
    def keys(self):
        return {items.key for items in self.items}

    @property
    def capacity(self):
        return len(self._slots)