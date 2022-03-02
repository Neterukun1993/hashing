from __future__ import annotations
import collections
from typing import List, Tuple, Iterator, Callable, Hashable, Any


class ChainedHashMap(collections.abc.MutableMapping):
    count: int
    table: List[List[Tuple[Hashable, Any]]]

    def __init__(self, hash_func: Callable[[Hashable], int]) -> None:
        self.hash = hash_func
        self.count = 0
        self.table = [[] for _ in range(1)]

    def __contains__(self, key: Hashable) -> bool:
        i = self.hash(key) % len(self.table)
        for k, v in self.table[i]:
            if k == key:
                return True
        return False

    def __getitem__(self, key: Hashable) -> Any:
        i = self.hash(key) % len(self.table)
        for k, v in self.table[i]:
            if k == key:
                return v
        raise KeyError

    def __setitem__(self, key: Hashable, value: Any) -> None:
        chain = self.table[self.hash(key) % len(self.table)]
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        chain.append((key, value))
        if self.count + 1 > len(self.table):
            self._resize()
        self.count += 1

    def __delitem__(self, key: Hashable) -> None:
        chain = self.table[self.hash(key) % len(self.table)]
        for i, (k, value) in enumerate(chain):
            if k == key:
                del chain[i]
                self.count -= 1
                return
        raise KeyError

    def __iter__(self) -> Iterator[Hashable]:
        for chain in self.table:
            for key, value in chain:
                yield key

    def __len__(self) -> int:
        return self.count

    def _resize(self) -> None:
        new_table: List[List[Tuple[Hashable, Any]]] = (
            [[] for _ in range(2 * self.count)]
        )
        for chain in self.table:
            for key, value in chain:
                new_table[self.hash(key) % len(new_table)].append((key, value))
        self.table, new_table = new_table, self.table
        del new_table
