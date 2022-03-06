from __future__ import annotations
import collections
from typing import List, Iterator, Callable, Optional, Hashable


class Null:
    _instance: Optional[Null] = None

    def __new__(cls) -> Null:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class HopscotchHashSet(collections.abc.MutableSet):
    H: int = 32
    count: int
    prev: List[int]
    table: List[Hashable]

    def __init__(self, hash_func: Callable[[Hashable], int]) -> None:
        self.hash = hash_func
        self.count = 0
        self.prev = [-1 for _ in range(self.H)]
        self.table = [Null() for _ in range(self.H)]

    def __contains__(self, key: Hashable) -> bool:
        i = self.hash(key) % len(self.table)
        for bit in range(self.H):
            idx = (i + bit) % len(self.table)
            if self.prev[idx] == i and self.table[idx] == key:
                return True
        return False

    def __iter__(self) -> Iterator[Hashable]:
        for key in self.table:
            if key is not Null():
                yield key

    def __len__(self) -> int:
        return self.count

    def _resize(self) -> None:
        size = 2
        while size < 3 * self.count:
            size *= 2
        new_prev: List[int] = [-1 for _ in range(size)]
        new_table: List[Hashable] = [Null() for _ in range(size)]

        self.prev, new_prev = new_prev, self.prev
        self.table, new_table = new_table, self.table
        self.count = 0
        for key in new_table:
            if key is not Null():
                self.add(key)
        del new_table, new_prev

    def _shiftdown(self, i: int, idx_empty: int) -> int:
        while (idx_empty - i) % len(self.table) >= self.H:
            idx = (idx_empty - self.H + 1) % len(self.table)
            for bit in range(self.H):
                hop = (idx + bit) % len(self.table)
                if self.prev[hop] == -1:
                    continue
                if idx < idx_empty and idx <= self.prev[hop]:
                    self.table[idx_empty], self.table[hop] = (
                        self.table[hop], self.table[idx_empty]
                    )
                    self.prev[idx_empty], self.prev[hop] = (
                        self.prev[hop], self.prev[idx_empty]
                    )
                    break
                if idx > idx_empty and (idx <= self.prev[hop] or self.prev[hop] <= idx_empty):
                    self.table[idx_empty], self.table[hop] = (
                        self.table[hop], self.table[idx_empty]
                    )
                    self.prev[idx_empty], self.prev[hop] = (
                        self.prev[hop], self.prev[idx_empty]
                    )
                    break
            else:
                raise KeyError('hash collision')
            idx_empty = hop
        return idx_empty

    def add(self, key: Hashable) -> None:
        if key in self:
            return
        if 2 * (self.count + 1) > len(self.table):
            self._resize()
        i = self.hash(key) % len(self.table)
        for w in range(len(self.table)):
            if self.table[(i + w) % len(self.table)] is Null():
                break
        idx_empty = self._shiftdown(i, (i + w) % len(self.table))
        self.count += 1
        self.prev[idx_empty] = i
        self.table[idx_empty] = key

    def discard(self, key: Hashable) -> None:
        i = self.hash(key) % len(self.table)
        for bit in range(self.H):
            idx = (i + bit) % len(self.table)
            if self.prev[idx] == i and self.table[idx] == key:
                self.prev[idx] = -1
                self.table[idx] = Null()
                self.count -= 1
                return
