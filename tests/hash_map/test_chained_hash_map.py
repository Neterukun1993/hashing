import pytest
from src.hash_function.integer_hash import hash_uint32
from src.hash_map.chained_hash_map import ChainedHashMap


@pytest.fixture
def hash_map():
    return ChainedHashMap(hash_uint32)


class TestChainedHashMap:

    def test_empty(self, hash_map):
        assert not hash_map

        hash_map[0] = 0
        assert hash_map

        del hash_map[0]
        assert not hash_map

    def test_length(self, hash_map):
        n = 30
        for key in range(n):
            value = key + 100
            assert len(hash_map) == key
            hash_map[key] = value

        for key in range(n):
            assert len(hash_map) == n - key
            del hash_map[key]

    def test_contains(self, hash_map):
        n = 30
        for key in range(n):
            value = key + 100
            assert key not in hash_map
            hash_map[key] = value
            assert key in hash_map

        for key in range(n):
            value = key + 100
            assert key in hash_map
            del hash_map[key]
            assert key not in hash_map

    def test_getitem(self, hash_map):
        n = 30
        for key in range(n):
            value = key + 100
            hash_map[key] = value
        for key in range(n):
            value = key + 100
            assert hash_map[key] == value

    def test_iterate(self, hash_map):
        n = 30
        builtin_dict = dict()
        for key in range(n):
            value = key + 100
            hash_map[key] = value
            builtin_dict[key] = value

        assert len(hash_map) == n
        for key in hash_map:
            assert hash_map[key] == builtin_dict[key]

    def test_clear(self, hash_map):
        n = 30
        for key in range(n):
            value = key + 100
            hash_map[key] = value

        assert hash_map

        hash_map.clear()
        assert not hash_map

    def test_setitem_duplicate(self, hash_map):
        hash_map[0] = 100
        assert len(hash_map) == 1
        assert hash_map[0] == 100

        hash_map[0] = 200
        assert len(hash_map) == 1
        assert hash_map[0] == 200

    def test_getitem_failed_if_map_not_contains_key(self, hash_map):
        with pytest.raises(KeyError):
            hash_map[0]

    def test_delitem_failed_if_map_not_contains_key(self, hash_map):
        with pytest.raises(KeyError):
            del hash_map[0]
