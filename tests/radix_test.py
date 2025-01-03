"""
Tests specific for Radix class.

These tests does not apply for parent classes (like Trie).
Such tests are included in trie-like and dict-like tests.
"""
from retrie.radix import Radix
from tests.test_utils import default_value


def test_radix_iternal_struct() -> None:

    keys = [
        "a",
        "abc",
        "abcd",
        "abcef",
        "c",
    ]

    trie = Radix({key: default_value(key) for key in keys})

    assert trie.data["a"] is trie.__getnode_safe__("a")

    assert trie.data["a"]["bc"].value == trie["abc"]

    assert "d" in trie.data["a"]["bc"]
    assert "ef" in trie.data["a"]["bc"]
