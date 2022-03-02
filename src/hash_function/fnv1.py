# https://en.wikipedia.org/wiki/Fowler–Noll–Vo_hash_function

MASK32 = 0xffffffff
BASIS32 = 0x811c9dc5
PRIME32 = 0x01000193

MASK64 = 0xffffffffffffffff
BASIS64 = 0xcbf29ce484222325
PRIME64 = 0x00000100000001B3


def fnv1_32(key: str) -> int:
    hash_ = BASIS32
    for byte in key.encode(encoding="utf-8"):
        hash_ = (hash_ * PRIME32) & MASK32
        hash_ ^= byte
    return hash_


def fnv1a_32(key: str) -> int:
    hash_ = BASIS32
    for byte in key.encode(encoding="utf-8"):
        hash_ ^= byte
        hash_ = (hash_ * PRIME32) & MASK32
    return hash_


def fnv1_64(key: str) -> int:
    hash_ = BASIS64
    for byte in key.encode(encoding="utf-8"):
        hash_ = (hash_ * PRIME64) & MASK64
        hash_ ^= byte
    return hash_


def fnv1a_64(key: str) -> int:
    hash_ = BASIS64
    for byte in key.encode(encoding="utf-8"):
        hash_ ^= byte
        hash_ = (hash_ * PRIME64) & MASK64
    return hash_
