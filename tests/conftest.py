"""Test config and fixtures used by tests."""
from typing import Iterable

import pytest

from triematch.radix import Radix
from tests.test_utils import (
    data_in_test,
    default_value,
    func_simple_radix,
    func_simple_trie,
    func_simple_tuple_trie,
)
from triematch.trie import Trie


@pytest.fixture()
def empty_trie() -> Trie:
    """Empty Trie fixture."""
    return Trie()


@pytest.fixture(params=[data_in_test.StrData.key_list])
def simple_trie(request: pytest.FixtureRequest) -> Trie:
    """Get A Trie based on list of keys passed to the fixture."""
    return func_simple_trie(keys=request.param)



@pytest.fixture(params=[Trie, Radix,])
def strtrie_like_class(request: pytest.FixtureRequest) -> Trie:
    """Trie-likes constructor classes that work with string sequeneces (not tuples)."""
    return request.param


@pytest.fixture(
    scope="function",
    params=[func_simple_trie, func_simple_tuple_trie, func_simple_radix],
)
def mutable_trie(request: pytest.FixtureRequest) -> Trie:
    """
    Get A Mutable Trie based on list of keys passed to the fixture.

    This includes StringTrie, TupleTrie and Radix.
    """
    return request.param


@pytest.fixture(
    scope="function",
    params=[func_simple_trie, func_simple_radix],
)
def any_trielike(request: pytest.FixtureRequest) -> Trie:
    """
    Fixture for iteration over all trie-like objects.

    Test object generator for all types of Trie-like classes.
    This is supposed to be used as parameter for other fixtures and
    create a test parameter matrix for other fixtures (like simple_trielike).
    """
    return request.param


@pytest.fixture(params=[data_in_test.StrData.key_list])
def simple_trielike(
    request: pytest.FixtureRequest,
    any_trielike: Trie,
) -> Trie:
    """Fixture to get all trie-like objects based on provided keys list."""
    return any_trielike(keys=request.param)

@pytest.fixture(params=[data_in_test.StrData.key_list])
def simple_mutable_trielike(request: pytest.FixtureRequest, mutable_trie: Trie) -> Trie:
    """
    Fixture to get all mutable trie-like objects based on provided keys list.

    This includes StringTrie, TupleTrie and Radix.
    """
    return mutable_trie(keys=request.param)


@pytest.fixture(params=[data_in_test.TupleStrData.key_list])
def simple_tuple_trie(request: pytest.FixtureRequest) -> Trie:
    """Get A TupleTrie based on list of keys passed to the fixture."""
    return func_simple_tuple_trie(keys=request.param)


@pytest.fixture(params=[data_in_test.StrData.key_list])
def simple_trie_keys(request: pytest.FixtureRequest) -> list:
    """Get A list of keys based on list of keys passed to the fixture."""
    return request.param


@pytest.fixture(params=[data_in_test.StrData.new_key])
def new_key(request: pytest.FixtureRequest) -> str:
    """Get a key which is not included in the key list used for creating the fixture."""
    return request.param


@pytest.fixture()
def long_key() -> Iterable:
    """Get a key which is longer than the keys in the key list."""
    return data_in_test.StrData.long_key


@pytest.fixture()
def missing_key() -> Iterable:
    """Get a key which is not included in the key list used for creating the fixture."""
    return data_in_test.StrData.missing_key

@pytest.fixture()
def default_value_func() -> callable:
    """
    Get the function used for generating default value.

    This function gets the key and returns corresponding value
    """
    return default_value
