import random


class TabulationHash:
    def __init__(self) -> None:
        self.tables = [[0] * 256 for _ in range(4)]
        self._initialize()

    def _initialize(self) -> None:
        for i in range(4):
            for j in range(256):
                self.tables[i][j] = random.randint(0, 0xffffffff)

    def rehash(self) -> None:
        self._initialize()

    def hash(self, key: int) -> int:
        h = 0
        for i in range(4):
            h ^= self.tables[i][key & 0xff]
            key >>= 8
        return h
