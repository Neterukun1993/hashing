import collections
from typing import List, Iterator, Callable, Hashable


class ChainedHashSet(collections.abc.MutableSet[Hashable]):
    count: int
    table: List[List[Hashable]]

    def __init__(self, hash_func: Callable[[Hashable], int]) -> None:
        self.hash = hash_func
        self.count = 0
        self.table = [[] for _ in range(1)]

    def __contains__(self, key: Hashable) -> bool:
        chain = self.table[self.hash(key) % len(self.table)]
        return key in chain

    def __iter__(self) -> Iterator[Hashable]:
        for chain in self.table:
            for key in chain:
                yield key

    def __len__(self) -> int:
        return self.count

    def _resize(self) -> None:
        new_table: List[List[Hashable]] = [[] for _ in range(2 * self.count)]
        for key in self:
            new_table[self.hash(key) % len(new_table)].append(key)
        self.table, new_table = new_table, self.table
        del new_table

    def add(self, key: Hashable) -> None:
        if key in self:
            return
        if self.count + 1 > len(self.table):
            self._resize()
        self.table[self.hash(key) % len(self.table)].append(key)
        self.count += 1

    def discard(self, key: Hashable) -> None:
        if key in self:
            chain = self.table[self.hash(key) % len(self.table)]
            del chain[chain.index(key)]
            self.count -= 1
