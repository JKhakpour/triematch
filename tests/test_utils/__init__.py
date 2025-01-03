"""Some utility functions for running tests."""
from typing import Callable, Iterable

from retrie.ahocorasick import ACTrie
from retrie.radix import Radix
from retrie.trie import Empty, Trie, TupleTrie
from tests.test_utils import data_in_test

Etc = data_in_test.Etc
PAD = "-"
NODE_SIGN = "."
STRIP_CHARS = None

def default_value(key: Iterable) -> Iterable:
    """Generate value for a given key. default is to key in reverse order."""
    return key[::-1]

def func_simple_trie(
    keys: Iterable=data_in_test.StrData.key_list,
    value_func: Callable=default_value,
) -> Trie:
    """Generate a Trie object with provided keys and values from value_func func."""
    return Trie({key: value_func(key) for key in keys})


def func_simple_ac_trie(
    keys: Iterable=data_in_test.StrData.key_list,
    value_func: Callable=default_value,
) -> ACTrie:
    """Generate a Aho-Corasick Trie object with provided keys."""
    return ACTrie({key: value_func(key) for key in keys})


def func_simple_radix(
    keys: Iterable=data_in_test.StrData.key_list,
    value_func: Callable=default_value,
) -> Radix:
    """Generate a Radix object with provided keys."""
    return Radix({key: value_func(key) for key in keys})


def func_simple_tuple_trie(
    keys: Iterable=data_in_test.StrData.key_list,
    value_func: Callable=default_value,
) -> TupleTrie:
    """Generate a TupleTrie object with provided keys."""
    return TupleTrie({key: value_func(key) for key in keys})


def print_nested(data: dict, lvl: int=0) -> str:
    """Print a nested dictionary (Tree) in a human readable indented format."""
    ret = ""
    for key, node in data.items():
        ret += (
            f"{PAD * lvl}{key}{NODE_SIGN if node.value is not Empty else ''}\n"
            + print_nested(node, lvl + 1)
        )
    if lvl == 0:
        return ret.strip(STRIP_CHARS)
    return ret
