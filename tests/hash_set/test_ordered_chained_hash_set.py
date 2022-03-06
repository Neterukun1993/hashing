import pytest
from src.hash_function.integer_hash import hash_uint32
from src.hash_set.ordered_chained_hash_set import OrderedChainedHashSet


@pytest.fixture
def hash_set():
    return OrderedChainedHashSet(hash_uint32)


class TestOrderedChainedHashSet:

    def test_empty(self, hash_set):
        assert not hash_set

        hash_set.add(0)
        assert hash_set

        hash_set.remove(0)
        assert not hash_set

    def test_length(self, hash_set):
        n = 30
        for value in range(n):
            assert len(hash_set) == value
            hash_set.add(value)

        for value in range(n):
            assert len(hash_set) == n - value
            hash_set.remove(value)

    def test_contains(self, hash_set):
        n = 30
        for value in range(n):
            assert value not in hash_set
            hash_set.add(value)
            assert value in hash_set

        for value in range(n):
            assert value in hash_set
            hash_set.remove(value)
            assert value not in hash_set

    def test_orderd_iterate(self, hash_set):
        from itertools import zip_longest

        n = 30
        builtin_set = set()
        for value in range(n):
            hash_set.add(value)
            builtin_set.add(value)

        assert(len(hash_set) == n)
        for v1, v2 in zip_longest(hash_set, builtin_set):
            assert v1 == v2

        builtin_set.remove(2)
        builtin_set.remove(15)
        builtin_set.remove(23)
        hash_set.remove(2)
        hash_set.remove(15)
        hash_set.remove(23)
        for v1, v2 in zip_longest(hash_set, builtin_set):
            assert v1 == v2

    def test_clear(self, hash_set):
        n = 30
        for value in range(n):
            hash_set.add(value)

        assert hash_set

        hash_set.clear()
        assert not hash_set

    def test_add_duplicate(self, hash_set):
        hash_set.add(0)
        assert(len(hash_set) == 1)

        hash_set.add(0)
        assert(len(hash_set) == 1)

    def test_remove_failed_if_set_not_contains_value(self, hash_set):
        with pytest.raises(KeyError):
            hash_set.remove(0)
