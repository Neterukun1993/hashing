from __future__ import annotations
import collections
from typing import List, Iterator, Callable, Hashable, Optional


class Null:
    _instance: Optional[Null] = None

    def __new__(cls) -> Null:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Deleted:
    _instance: Optional[Deleted] = None

    def __new__(cls) -> Deleted:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class LinearProbingHashSet(collections.abc.MutableSet):
    n: int
    q: int
    table: List[Hashable]

    def __init__(self, hash_func: Callable[[Hashable], int]) -> None:
        self.hash = hash_func
        self.n = 0
        self.q = 0
        self.table = [Null() for _ in range(2)]

    def __contains__(self, key: Hashable) -> bool:
        i = self.hash(key) % len(self.table)
        while self.table[i] is not Null():
            if self.table[i] is not Deleted() and self.table[i] == key:
                return True
            i = (i + 1) % len(self.table)
        return False

    def __iter__(self) -> Iterator[Hashable]:
        for key in self.table:
            if key is not Null() and key is not Deleted():
                yield key

    def __len__(self) -> int:
        return self.n

    def _resize(self) -> None:
        size = 2
        while size < 3 * self.n:
            size *= 2
        table: List[Hashable] = [Null() for _ in range(size)]

        self.q = 0
        for key in self:
            i = self.hash(key) % len(table)
            while table[i] is not Null():
                i = (i + 1) % len(table)
            table[i] = key
        self.table, table = table, self.table
        del table

    def add(self, key: Hashable) -> None:
        if key in self:
            return
        if 2 * (self.q + 1) > len(self.table):
            self._resize()
        i = self.hash(key) % len(self.table)
        while self.table[i] is not Null() and self.table[i] is not Deleted():
            i = (i + 1) % len(self.table)
        if self.table[i] is Null():
            self.q += 1
        self.n += 1
        self.table[i] = key

    def discard(self, key: Hashable) -> None:
        i = self.hash(key) % len(self.table)
        while self.table[i] is not Null():
            if self.table[i] is not Deleted() and self.table[i] == key:
                self.table[i] = Deleted()
                self.n -= 1
                if 8 * self.n < len(self.table):
                    self._resize()
                break
            i = (i + 1) % len(self.table)
