"""
Tests for Trie-like classes.

These tests check general behavior of Trie class and its subclasses.
"""
from types import GeneratorType

from retrie import Trie, TupleTrie
from tests.test_utils import (
    default_value,
    print_nested,
)
from retrie.trie import Node


def test_trie_dunder_copy_is_not_shallow(simple_trielike, long_key) -> None:
    """
    test if trie.__copy__ is doing a shallow copy or a doing copy on all levels
    of nested dicts (Nodes)
    """
    trie2 = simple_trielike.__copy__()
    assert trie2 == simple_trielike
    assert trie2 is not simple_trielike

    assert isinstance(trie2, simple_trielike.__class__)
    assert isinstance(trie2.data, simple_trielike.data.__class__)

    original_nodes = simple_trielike._traverse_nodes(long_key, only_leafs=False)
    copied_nodes = trie2._traverse_nodes(long_key, only_leafs=False)

    for (orig_len, original_node), (copy_len, copied_node) in zip(
        original_nodes,
        copied_nodes,
    ):
        assert orig_len == copy_len

        assert (
            original_node is not copied_node
        ), f"node data for original trie and copied trie are \
            same object in subkey {long_key[:orig_len]}"

        assert (
            original_node == copied_node
        ), f"node data for original trie and copied trie is \
            different in subkey {long_key[:orig_len]}"


def test_trie_dot_data_internal_structure() -> None:
    keys = [
        "aab",
        "abb",
        "abc",
        "abcdef",
        "abd",
    ]
    expected_struct = """
    a
    -a
    --b.
    -b
    --b.
    --c.
    ---d
    ----e
    -----f.
    --d.
    """.replace(
        " ", "",
    ).strip()
    trie = Trie({k: default_value(k) for k in keys})
    structure = print_nested(trie.data)
    assert isinstance(trie.data, Node)
    assert expected_struct == structure


def test_tuple_trie_dot_data_internal_structure() -> None:
    keys = [
        (1, 1, 2),
        (1, 2, 2),
        (1, 2, 3),
        (1, 2, 3, "X", None, 156),
        (1, 2, "d"),
    ]
    expected_struct = """
    1
    -1
    --2.
    -2
    --2.
    --3.
    ---X
    ----None
    -----156.
    --d.
    """.replace(
        " ", "",
    ).strip()
    trie = TupleTrie({k: default_value(k) for k in keys})
    structure = print_nested(trie.data)
    assert isinstance(trie.data, Node)
    assert expected_struct == structure


def test_traverse_path() -> None:
    keys = [
        "ab",
        "abb",
        "abc",
        "abcdef",
        "abd",
        "bc",
    ]
    trie = Trie({k: default_value(k) for k in keys})
    search_text = "abcdefghi"
    path = trie.match(search_text)

    assert isinstance(
        path, GeneratorType,
    ), "trie.match() result is supposed to be a generator"
    for match_len, value in path:
        assert match_len <= len(
            search_text,
        ), f"match_len {match_len} exceeds search_text length {len(search_text)}"
        key = search_text[:match_len]
        assert (
            default_value(key) == value
        ), f"expected value for '{key=}' does not match returned {value=}"


def test_trie_to_regex(strtrie_like_class) -> None:
    trie = strtrie_like_class({"ab": 1, "ac": 1})
    pattern = trie.to_regex()
    assert pattern == "a[bc]"


def test_trie_to_regex2(strtrie_like_class) -> None:
    trie = strtrie_like_class({"abc": 1, "ac": 1})
    pattern = trie.to_regex()
    assert pattern == "a(?:bc|c)"


def test_trie_to_regex3(strtrie_like_class) -> None:
    trie = strtrie_like_class({"aabc": 1, "ac": 1})
    pattern = trie.to_regex()
    assert pattern == "a(?:abc|c)"


def test_trie_to_regex4(strtrie_like_class) -> None:
    trie = strtrie_like_class({"aabc": 1, "aab": 1, "acd": 1})
    pattern = trie.to_regex()
    assert pattern == "a(?:ab|cd)"


def test_trie_to_regex5(strtrie_like_class) -> None:
    trie = strtrie_like_class({"ab": 1, "ac": 1, "de": 1, "f": 1})
    pattern = trie.to_regex()
    assert pattern == "a[bc]|de|f"


def test_trie_to_regex6(strtrie_like_class) -> None:
    ## in this test, it should ignore longer key that includes a sorter key
    ## this means if it has 'abcdef' then it already
    # has 'abc', so we just need to check 'abc'
    trie = strtrie_like_class({"ab": 1, "abc": 1, "abcdef": 1, "f": 1})
    pattern = trie.to_regex()
    assert pattern == "ab|f"


def test_trie_to_regex7(strtrie_like_class) -> None:
    ## in this test, it should ignore longer key that includes a sorter key
    ## this means if it has 'abcdef' then it already
    # has 'abc', so we just need to check 'abc'
    trie = strtrie_like_class({"abbc": 1, "abbbbcc": 1})
    pattern = trie.to_regex()
    assert pattern == "abb(?:bbcc|c)"


def test_trie_match(strtrie_like_class) -> None:

    keys = [
        "a",
        "ab",
        "abc",
        "bcd",
    ]
    text = "abcdecfgh"
    trie = strtrie_like_class({key: default_value(key) for key in keys})

    assert list(trie.match(text)) == [
        (1, default_value("a")),
        (2, default_value("ab")),
        (3, default_value("abc")),
    ]

    assert list(trie.match(text[1:])) == [
        (3, default_value("bcd")),
    ]


def test_trie_search(strtrie_like_class) -> None:

    keys = [
        "a",
        "ab",
        "abc",
        "abd",
        "abcd",
        "bcd",
        "c",
    ]
    text = "abbcdecfgh"
    trie = strtrie_like_class({key: default_value(key) for key in keys})

    assert list(trie.search(text)) == [
        (0, 1, default_value("a")),
        (0, 2, default_value("ab")),
        (2, 5, default_value("bcd")),
        (3, 4, default_value("c")),
        (6, 7, default_value("c")),
    ]
