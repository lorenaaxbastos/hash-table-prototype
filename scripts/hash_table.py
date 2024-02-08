from typing import NamedTuple, Any
from collections import deque

class Pair(NamedTuple):
    key: Any
    value: Any

class HashTable:        
    @classmethod
    def from_dict(cls, dictionary, capacity=None):
        hashtable = cls(capacity or len(dictionary))
        for key, value in dictionary.items():
            hashtable[key] = value
        return hashtable
        
    def __init__(self, capacity=8, load_factor_threshold=0.6):
        if capacity <= 0:
            raise ValueError("Capacity should be a positive number and greater than zero.")
        if not (0 < load_factor_threshold <= 1):
            raise ValueError("Load factor must be a number between 0 and 1.")
        self._keys = []
        self._buckets = [deque() for _ in range(capacity)]
        self._load_factor_threshold = load_factor_threshold

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        return self.items == other.items

    def __str__(self):
        items = []
        for key, value in self.items:
            items.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(items) + "}"

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"
    
    def __iter__(self):
        yield from self.keys

    def __len__(self):
        return len(self.items)

    def __setitem__(self, key, value):
        if self.load_factor >= self._load_factor_threshold:
            self._resize_and_rehash()
            
        bucket = self._buckets[self._index(key)]
        for i, item in enumerate(bucket):
            if item.key == key:
                bucket[i] = Pair(key, value)
                break
        else:
            bucket.append(Pair(key, value))
            self._keys.append(key)

    def __getitem__(self, key):
        bucket = self._buckets[self._index(key)]
        for item in bucket:
            if item.key == key:
                return item.value
        raise KeyError(key)

    def __delitem__(self, key):
        bucket = self._buckets[self._index(key)]
        for i, item in enumerate(bucket):
            if item.key == key:
                del bucket[i]
                self._keys.remove(key)
                break
        else:
            raise KeyError(key)

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def _index(self, key):
        return hash(key) % self.capacity

    def _resize_and_rehash(self):
        copy = HashTable(capacity=self.capacity * 2)
        for key, value in self.items:
            copy[key] = value
        self._buckets = copy._buckets

    def copy(self):
        return HashTable.from_dict(dict(self.items), self.capacity)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self):
        self._buckets = [deque() for _ in range(self.capacity)]
        self._keys = []

    def update(self, dictionary):
        for key, value in dictionary.items():
            self[key] = value

    @property
    def items(self):
        return [(key, self[key]) for key in self._keys]

    @property
    def values(self):
        return [self[key] for key in self._keys]

    @property
    def keys(self):
        return self._keys.copy()

    @property
    def capacity(self):
        return len(self._buckets)

    @property
    def load_factor(self):
        return len(self) / self.capacity