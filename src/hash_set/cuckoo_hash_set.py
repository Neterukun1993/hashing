from __future__ import annotations
import collections
from typing import Protocol, List, Iterator, Hashable, Optional, Any


class Rehashing(Protocol):
    def __init__(self) -> None: ...

    def rehash(self) -> None: ...

    def hash(self, key: Any) -> int: ...


class Null:
    _instance: Optional[Null] = None

    def __new__(cls) -> Null:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class CuckooHashSet(collections.abc.MutableSet):
    MAXLOOP: int = 100
    count: int
    hashing1: Rehashing
    hashing2: Rehashing
    table1: List[Hashable]
    table2: List[Hashable]

    def __init__(self, hashing1: Rehashing, hashing2: Rehashing) -> None:
        self.count = 0
        self.hashing1 = hashing1
        self.hashing2 = hashing2
        self.table1 = [Null() for _ in range(2)]
        self.table2 = [Null() for _ in range(2)]

    def __contains__(self, key: Hashable) -> bool:
        h1 = self.hashing1.hash(key) % len(self.table1)
        h2 = self.hashing2.hash(key) % len(self.table2)
        return self.table1[h1] == key or self.table2[h2] == key

    def __iter__(self) -> Iterator[Hashable]:
        for key in self.table1:
            if key is not Null():
                yield key
        for key in self.table2:
            if key is not Null():
                yield key

    def __len__(self) -> int:
        return self.count

    def _resize(self) -> None:
        table1: List[Hashable] = [Null() for _ in range(2 * self.count)]
        table2: List[Hashable] = [Null() for _ in range(2 * self.count)]
        count = self.count
        self.table1, table1 = table1, self.table1
        self.table2, table2 = table2, self.table2

        for key in table1:
            if key is not Null():
                self.add(key)
        for key in table2:
            if key is not Null():
                self.add(key)
        self.count = count
        del table1, table2

    def _rehash(self) -> None:
        self.hashing1.rehash()
        self.hashing2.rehash()

        table1: List[Hashable] = [Null() for _ in range(self.count)]
        table2: List[Hashable] = [Null() for _ in range(self.count)]
        count = self.count
        self.table1, table1 = table1, self.table1
        self.table2, table2 = table2, self.table2

        for key in table1:
            if key is not Null():
                self.add(key)
        for key in table2:
            if key is not Null():
                self.add(key)
        self.count = count
        del table1, table2

    def add(self, key: Hashable) -> None:
        if key in self:
            return
        if self.count + 1 > len(self.table1):
            self._resize()
        for loop in range(self.MAXLOOP):
            h1 = self.hashing1.hash(key) % len(self.table1)
            h2 = self.hashing2.hash(key) % len(self.table2)
            if loop % 2 == 0:
                if self.table1[h1] is Null():
                    self.table1[h1] = key
                    self.count += 1
                    return
                else:
                    key, self.table1[h1] = self.table1[h1], key
            else:
                if self.table2[h2] is Null():
                    self.table2[h2] = key
                    self.count += 1
                    return
                else:
                    key, self.table2[h2] = self.table2[h2], key
        self._rehash()
        self.add(key)

    def discard(self, key: Hashable) -> None:
        h1 = self.hashing1.hash(key) % len(self.table1)
        h2 = self.hashing2.hash(key) % len(self.table2)
        if self.table1[h1] == key:
            self.count -= 1
            self.table1[h1] = Null()
        if self.table2[h2] == key:
            self.count -= 1
            self.table2[h2] = Null()
