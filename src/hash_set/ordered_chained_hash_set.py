from __future__ import annotations
import collections
from typing import List, Iterator, Callable, Hashable


class DLLNode:
    value: Hashable
    prv: DLLNode
    nxt: DLLNode

    def __init__(self, value: Hashable) -> None:
        self.value = value
        self.prv, self.nxt = self, self


class DoublyLinkedList:
    size: int
    dummy: DLLNode

    def __init__(self) -> None:
        self.size = 0
        self.dummy = DLLNode(0)

    def __iter__(self) -> Iterator[DLLNode]:
        node = self.dummy.nxt
        while node is not self.dummy:
            yield node
            node = node.nxt

    def last(self) -> DLLNode:
        return self.dummy.prv

    def remove(self, node: DLLNode) -> None:
        node.prv.nxt = node.nxt
        node.nxt.prv = node.prv
        self.size -= 1

    def append(self, value: Hashable) -> None:
        new = DLLNode(value)
        new.prv = self.dummy.prv
        new.nxt = self.dummy
        new.prv.nxt = new
        new.nxt.prv = new
        self.size += 1


class OrderedChainedHashSet(collections.abc.MutableSet):
    count: int
    _list: DoublyLinkedList
    table: List[List[DLLNode]]

    def __init__(self, hash_func: Callable[[Hashable], int]) -> None:
        self.hash = hash_func
        self.count = 0
        self._list = DoublyLinkedList()
        self.table = [[] for _ in range(1)]

    def __contains__(self, key: Hashable) -> bool:
        chain = self.table[self.hash(key) % len(self.table)]
        for node in chain:
            if node.value == key:
                return True
        return False

    def __iter__(self) -> Iterator[Hashable]:
        for node in self._list:
            yield node.value

    def __len__(self) -> int:
        return self.count

    def _resize(self) -> None:
        new_table: List[List[DLLNode]] = [[] for _ in range(2 * self.count)]
        for node in self._list:
            new_table[self.hash(node.value) % len(new_table)].append(node)
        self.table, new_table = new_table, self.table
        del new_table

    def add(self, key: Hashable) -> None:
        if key in self:
            return
        if self.count + 1 > len(self.table):
            self._resize()
        self._list.append(key)
        self.table[self.hash(key) % len(self.table)].append(self._list.last())
        self.count += 1

    def discard(self, key: Hashable) -> None:
        chain = self.table[self.hash(key) % len(self.table)]
        for i, node in enumerate(chain):
            if node.value == key:
                self._list.remove(node)
                del chain[i]
                self.count -= 1
                return
