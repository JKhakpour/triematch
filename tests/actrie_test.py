"""
Tests specific to ACTrie class and it's subclasses.
Most tests for ACTrie class can be found in trie-like and dict-like tests.
"""
import pytest

from retrie import ACTrie
from retrie.ahocorasick import ACTrieStates
from retrie.tests.test_utils import default_value


def test_actrie_link_state() -> None:
    """ACTrie link state changes to Linked after link_nodes have been executed"""
    keys = [
        "a",
        "ab",
        "abc",
    ]

    trie = ACTrie({key: default_value(key) for key in keys})
    trie.link_nodes()

    assert trie._state == ACTrieStates.Linked


def test_actrie_link_error_on_delete() -> None:

    keys = [
        "a",
        "ab",
        "abc",
    ]

    trie = ACTrie({key: default_value(key) for key in keys})
    trie.link_nodes()
    with pytest.raises(AttributeError):
        del trie["abc"]


def test_actrie_link_error_on_update() -> None:

    keys = [
        "a",
        "ab",
        "abc",
    ]

    trie = ACTrie({key: default_value(key) for key in keys})
    trie.link_nodes()
    new_value = trie["abc"] + trie["abc"]
    with pytest.raises(AttributeError):
        trie["abc"] = new_value


def test_actrie_unlink_state() -> None:

    keys = [
        "a",
        "ab",
        "abc",
    ]

    trie = ACTrie({key: default_value(key) for key in keys})
    trie.link_nodes()
    trie.unlink_nodes()
    assert trie._state == ACTrieStates.Not_Linked


def test_actrie_unlink_state_is_alterable() -> None:

    keys = [
        "a",
        "ab",
        "abc",
    ]

    trie = ACTrie({key: default_value(key) for key in keys})
    trie.link_nodes()
    trie.unlink_nodes()
    new_value = trie["abc"] + trie["abc"]
    trie["abc"] = new_value
    assert trie["abc"] == new_value


def test_actrie_failure_link() -> None:

    keys = [
        "a",
        "ab",
        "abc",
        "abd",
        "abcd",
        "bbbbac",
        "bcd",
        "c",
        "efgh",
    ]

    trie = ACTrie({key: default_value(key) for key in keys})
    trie.link_nodes()

    assert trie.data.failure_link is trie.data

    assert trie.__getnode_safe__("ab").failure_link is trie.__getnode_safe__("b")
    assert trie.__getnode_safe__("abcd").failure_link == trie.__getnode_safe__("bcd")
    assert trie.__getnode_safe__("bbbbac").failure_link == trie.__getnode_safe__("c")

    assert trie.__getnode_safe__("efgh").failure_link is trie.__getnode_safe__(
        "",
    )  # trie.data or root_node


def test_actrie_dictionary_link() -> None:

    keys = [
        "a",
        "ab",
        "abcd",
        "ac",
        "bbac",
        "bc",
    ]

    trie = ACTrie({key: default_value(key) for key in keys})
    trie.link_nodes()

    assert trie.data.dict_link is None

    assert trie.__getnode_safe__("ab").dict_link is None
    assert trie.__getnode_safe__("abc").dict_link == trie.__getnode_safe__("bc")
    assert trie.__getnode_safe__("abcd").dict_link is None
    assert trie.__getnode_safe__("bbac").dict_link == trie.__getnode_safe__("ac")


def test_actrie_search() -> None:

    keys = [
        "a",
        "abc",
        "abd",
        "abcd",
        "bcd",
        "c",
    ]
    text = "ababcdecfgh"
    trie = ACTrie({key: default_value(key) for key in keys})
    trie.link_nodes()

    assert list(trie.search(text)) == [
        (0, 1, default_value("a")),
        (2, 3, default_value("a")),
        (2, 5, default_value("abc")),
        (4, 5, default_value("c")),
        (2, 6, default_value("abcd")),
        (3, 6, default_value("bcd")),
        (7, 8, default_value("c")),
    ]
