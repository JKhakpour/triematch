"""Tests specific for Trie class which does not apply to it's subclasses."""
from retrie.tests.test_utils import default_value
from retrie.trie import Trie, TupleTrie


def test_trie_iternal_struct() -> None:

    keys = [
        "a",
        "abc",
        "abcd",
        "abce",
        "c",
    ]

    trie = Trie({key: default_value(key) for key in keys})

    assert trie.data["a"] is trie.__getnode_safe__("a")

    assert trie.data["a"]["b"]["c"].value == trie["abc"]

    assert "d" in trie.data["a"]["b"]["c"]
    assert "e" in trie.data["a"]["b"]["c"]


def test_tuple_trie_iternal_struct() -> None:

    keys = [
        (1,),
        (1, 2, 3),
        (1, 2, 3, 4),
        (1, 2, 3, 5),
        (3,),
    ]

    trie = TupleTrie({key: default_value(key) for key in keys})

    assert trie.data[1] is trie.__getnode_safe__((1,))

    assert trie.data[1][2][3].value == trie[(1, 2, 3)]

    assert 4 in trie.data[1][2][3]
    assert 5 in trie.data[1][2][3]
