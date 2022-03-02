# https://github.com/h2database/h2database/blob/master/h2/src/test/org/h2/test/store/CalculateHashConstant.java
# https://xoshiro.di.unimi.it/splitmix64.c

def hash_uint32(x: int) -> int:
    x = (((x >> 16) ^ x) * 0x45d9f3b) & 0xffffffff
    x = (((x >> 16) ^ x) * 0x45d9f3b) & 0xffffffff
    x = (x >> 16) ^ x
    return x


def hash_uint64(x: int) -> int:
    x = (x + 0x9e3779b97f4a7c15) & 0xffffffffffffffff
    x = ((x ^ (x >> 30)) * 0xbf58476d1ce4e5b9) & 0xffffffffffffffff
    x = ((x ^ (x >> 27)) * 0x94d049bb133111eb) & 0xffffffffffffffff
    x = x ^ (x >> 31)
    return x
