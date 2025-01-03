"""
All tests for dict like behavior of BaseTrie
(Trie, Radix, etc.) class and it's subclasses
"""

from collections.abc import KeysView, ValuesView

import pytest

from tests.test_utils import (
    data_in_test,
    default_value,
    func_simple_trie,
)

Etc = data_in_test.Etc


def test_data_in_test() -> None:
    for long_key, missing_key, key_list in zip(
        data_in_test.ALLTypes.long_keys,
        data_in_test.ALLTypes.missing_keys,
        data_in_test.ALLTypes.key_lists,
    ):
        assert (
            long_key in key_list
        ), f"updated data_in_test module? {long_key=} \
            has to be included in {key_list=}"
        assert (
            missing_key not in key_list
        ), f"updated data_in_test module? {missing_key=} \
            has to be not included in {key_list=}"
        assert (
            len(key_list) > 2
        ), "updated data_in_test module? some tests \
            require key_list to have at least 3 keys"


def test_make_trie_empty_contructor(
    strtrie_like_class,
    simple_trie_keys,
    default_value_func,
) -> None:
    """Create empty object and fill it later."""
    trie = strtrie_like_class()
    assert not trie, "Empty trie should eb evaluated as False"
    for k in simple_trie_keys:
        trie[k] = default_value_func(k)
    assert trie, "Non-empty trie should eb evaluated as True"


def test_make_trie_non_empty_constructor(
    strtrie_like_class,
    simple_trie_keys,
    default_value_func,
) -> None:
    """
    All kinds of passing data to trie should return equal result: a non-empty
        trie object with similar values.
    """
    kwargs = {k: default_value_func(k) for k in simple_trie_keys}
    trie1 = strtrie_like_class(kwargs)
    trie2 = strtrie_like_class(**kwargs)
    trie3 = strtrie_like_class(kwargs, **kwargs)
    assert trie1, "trie not created?"
    assert trie1 == trie2
    assert trie1 == trie3


def test_wrong_key_not_in_trie(simple_trielike, missing_key) -> None:
    """If key is not stored in trie, key in trie has to return False."""
    assert (
        missing_key not in simple_trielike
    ), f"key {missing_key} was supposed to be not in trie"


def test_longer_key_not_in_trie(simple_trielike, simple_trie_keys) -> None:
    """If key is not stored in trie, key in trie has to return False."""
    test_key = simple_trie_keys[-1]
    while test_key in simple_trie_keys:
        # After while loop this key should not be in trie
        test_key += "o"
    assert (
        test_key not in simple_trielike
    ), f"key {test_key} was supposed to be not in trie"


def test_subkey_not_in_trie(simple_trielike, simple_trie_keys) -> None:
    """If key is not stored in trie, key in trie has to return False."""
    test_key = max(simple_trie_keys, key=len)  ## longest key in trie
    while test_key in simple_trie_keys:
        # After while loop this key should not be in trie
        test_key = test_key[-1]
    assert (
        test_key
    ), "simple_trie_keys has to include some subkeys \
        not in the list (and corresponding trie)"
    assert (
        test_key not in simple_trielike
    ), f"key {test_key} was supposed to be not in trie"


def test_trie_get_value(simple_trielike, simple_trie_keys) -> None:
    """All keys in trie have to return their respective default values."""
    for key in simple_trie_keys:
        value = default_value(key)
        assert (
            simple_trielike[key] == value
        ), f"{value=} was expected as value of key {key=}"


def test_trie_get_wrong_key(simple_trielike, missing_key) -> None:
    """Reading missing_key from trie should raise KeyError."""
    with pytest.raises(KeyError):
        simple_trielike[missing_key]


@pytest.mark.parametrize(
    ("simple_trielike", "new_key"),
    zip(data_in_test.ALLTypes.key_lists, data_in_test.ALLTypes.new_keys),
    indirect=True,
)
def test_update_trie_simple_case(simple_trielike, new_key) -> None:
    """
    Tests whether a new key can be successfully added to
    the trie using the update method.
    """
    assert (
        new_key not in simple_trielike
    ), "this key was supposed to be missing in trie! (maybe wrong test data?)"
    simple_trielike.update({new_key: "new_val"})
    assert (
        new_key in simple_trielike
    ), "a new key added to the trie, but it is missing there"


@pytest.mark.parametrize(
    ("simple_trielike", "simple_trie_keys"),
    zip(data_in_test.ALLTypes.key_lists, data_in_test.ALLTypes.key_lists),
    indirect=True,
)
def test_update_val_in_trie(simple_trielike, simple_trie_keys) -> None:
    """
    Test the update functionality of a trie-like structure by.

    Changing the value associated with an existing key and verifying the change.
    """
    key = simple_trie_keys[0]
    assert (
        key in simple_trielike
    ), f"{key=} from simple_trie_keys not included in simple_trielike object?"

    current_val = simple_trielike[key]
    new_val = "new_val"
    assert current_val != new_val

    simple_trielike.update({key: new_val})
    assert key in simple_trielike
    assert simple_trielike[key] == new_val


def test_simpletrie_dot_items(
    simple_trielike,
    simple_trie_keys,
    default_value_func,
) -> None:
    values = [default_value_func(k) for k in simple_trie_keys]
    items = list(simple_trielike.items())

    assert len(items) == len(values)
    assert {val for key, val in items} == set(values)


def test_simpletrie_items_type(
    simple_trielike,
    simple_trie_keys,
    default_value_func,
) -> None:
    values = [default_value_func(k) for k in simple_trie_keys]
    items = list(simple_trielike.items())

    assert len(items) == len(values)
    assert {val for key, val in items} == set(values)


def test_simpletrie_to_dict(simple_trielike) -> None:
    dict_obj = dict(simple_trielike)

    assert simple_trielike == dict_obj


def test_simpletrie_to_dict_lw_unpack(simple_trielike) -> None:
    dict_obj = dict(**simple_trielike)

    assert simple_trielike == dict_obj


def test_trie_dot_keys(simple_trielike, simple_trie_keys) -> None:
    keys = simple_trielike.keys()

    assert type(keys) is KeysView
    assert set(keys) == set(simple_trie_keys)


def test_trie_dot_values(simple_trielike, simple_trie_keys) -> None:
    vals = simple_trielike.values()

    assert type(vals) is ValuesView
    assert set(vals) == {default_value(k) for k in simple_trie_keys}


@pytest.mark.parametrize(
    "simple_trie_keys",
    data_in_test.ALLTypes.key_lists,
    indirect=True,
)
def test_update_trie_colliding_key(strtrie_like_class, simple_trie_keys) -> None:
    """
    because it is a trie data strcture, make sure it is not \
    returning data from other similar keys.
    """
    trie = strtrie_like_class({key: default_value(key) for key in simple_trie_keys[:2]})
    new_key = simple_trie_keys[0] + simple_trie_keys[1] + simple_trie_keys[2]
    assert new_key not in trie
    new_val = "new_val"
    trie.update({new_key: new_val})
    assert new_key in trie
    assert new_val == trie[new_key]
    assert new_key + simple_trie_keys[0] not in trie


@pytest.mark.parametrize(
    ("simple_mutable_trielike", "simple_trie_keys"),
    zip(data_in_test.ALLTypes.key_lists, data_in_test.ALLTypes.key_lists),
    indirect=True,
)
def test_delete_key(simple_mutable_trielike, simple_trie_keys) -> None:
    key_to_delete = simple_trie_keys[-1]

    assert key_to_delete in simple_mutable_trielike
    del simple_mutable_trielike[key_to_delete]
    assert key_to_delete not in simple_mutable_trielike


def test_delete_key_with_resembling_keys(strtrie_like_class, simple_trie_keys) -> None:
    key_similar = "abababcc"
    key_to_delete = "aba_abcc"
    keys = (*simple_trie_keys, key_similar, key_to_delete)
    trie = strtrie_like_class({key: default_value(key) for key in keys})

    assert key_to_delete in trie

    del trie[key_to_delete]
    assert key_to_delete not in trie
    assert key_similar in trie


def test_delete_key_with_resembling_keys_text_count_len(
    strtrie_like_class,
    simple_trie_keys,
) -> None:
    key_similar = "abababcc"
    key_to_delete = "aba_abcc"
    keys = (*simple_trie_keys, key_similar, key_to_delete)
    trie = strtrie_like_class({key: default_value(key) for key in keys})

    assert len(trie) == len(keys)
    assert trie.count() == len(keys)

    del trie[key_to_delete]
    assert len(trie) == len(keys) - 1
    assert trie.count() == len(keys) - 1


def testfunc_simple_trie_dunder_or(simple_trie) -> None:
    assert (simple_trie or ...) is simple_trie


def test_empty_trie_dunder_or(empty_trie) -> None:
    assert (empty_trie or ...) is ...


def test_similar_tries_dunder_eq() -> None:
    simple_trie1 = func_simple_trie()
    simple_trie2 = func_simple_trie()
    assert simple_trie1 is not simple_trie2

    assert simple_trie1 == simple_trie2


def test_trie_dot_get_existing_key(simple_trielike, simple_trie_keys) -> None:
    existing_key = simple_trie_keys[0]
    assert simple_trielike.get(existing_key, Etc) == default_value(existing_key)


def test_trie_dot_get_missing_key(simple_trielike, new_key) -> None:
    # new_key does not exist in trie object
    assert new_key not in simple_trielike
    assert simple_trielike.get(new_key, Etc) == Etc


def test_trie_dot_update(simple_trielike, new_key) -> None:
    value = 123
    simple_trielike[new_key] = value
    assert new_key in simple_trielike
    assert simple_trielike[new_key] == value


def test_trie_dot_setdefault(simple_trielike, simple_trie_keys, new_key) -> None:
    key = simple_trie_keys[0]

    assert simple_trielike.setdefault(key, 1) != 1
    assert simple_trielike.setdefault(new_key, 1) == 1
    assert simple_trielike.setdefault(new_key) == 1


def test_trie_repr(strtrie_like_class, new_key) -> None:
    val = default_value(new_key)
    dct = {new_key: val}

    trie = strtrie_like_class()
    assert str(trie) == "{}"
    trie[new_key] = val
    assert str(trie) == str(dct)


def test_trie_dot_pop(simple_mutable_trielike, simple_trie_keys) -> None:
    key = simple_trie_keys[0]
    trie_length = len(simple_mutable_trielike)

    assert simple_mutable_trielike.pop(key, ...) == default_value(key)
    assert simple_mutable_trielike.pop(key, ...) == ...
    assert len(simple_mutable_trielike) == trie_length - 1


def test_trie_dot_clear(simple_mutable_trielike) -> None:
    assert simple_mutable_trielike.count() > 0
    simple_mutable_trielike.clear()
    assert simple_mutable_trielike.count() == 0


def test_trie_dot_copy(simple_trielike) -> None:
    trie2 = simple_trielike.copy()

    assert trie2 is not simple_trielike

    assert trie2 == simple_trielike

    assert isinstance(trie2, simple_trielike.__class__)
    assert isinstance(trie2.data, simple_trielike.data.__class__)


def test_trie_dot_copy_and_modify(simple_mutable_trielike, simple_trie_keys) -> None:
    key = simple_trie_keys[0]
    trie2 = simple_mutable_trielike.copy()

    assert trie2 is not simple_mutable_trielike

    assert trie2 == simple_mutable_trielike
    assert isinstance(trie2, simple_mutable_trielike.__class__)
    assert isinstance(trie2.data, simple_mutable_trielike.data.__class__)

    trie2.pop(key)
    assert trie2 != simple_mutable_trielike


def test_trie_dunder_copy(simple_trie, simple_trie_keys) -> None:
    key = simple_trie_keys[0]
    trie2 = simple_trie.__copy__()
    assert trie2 is not simple_trie
    assert trie2 == simple_trie
    assert isinstance(trie2, simple_trie.__class__)
    assert isinstance(trie2.data, simple_trie.data.__class__)

    trie2.pop(key)
    assert trie2 != simple_trie


def test_trie_dunder_copy_is_not_copying_values(simple_trielike, long_key) -> None:
    """
    copy & __copy__ are doing it in multiple levels,
    but they should not copy the value object
    """
    key = long_key  # some random key
    other_key = "this_key_is outside_trie"
    other_val = "ABCD"

    simple_trielike[key] = {}  # try it with a mutable object

    trie2 = simple_trielike.__copy__()
    assert trie2 == simple_trielike
    assert trie2 is not simple_trielike

    assert trie2[key] == simple_trielike[key] == {}
    assert trie2[key] is simple_trielike[key]

    trie2[key][other_key] = other_val
    assert trie2[key] is simple_trielike[key]
    assert other_key in simple_trielike[key]


@pytest.mark.parametrize(
    ("simple_trie", "simple_trie_keys"),
    [
        (data_in_test.StrData.key_list, data_in_test.StrData.key_list),
    ],
    indirect=True,
)
def test_trie_extend_key(simple_trie, simple_trie_keys) -> None:
    """
    test if Trie.extend returns expedted list of keys for string keys.
    Trie class is a StringTrie and it is expected to work fine in .items(<str key>)
    """
    for explore_key in simple_trie_keys:
        for _ in range(1, len(explore_key)):
            explored_keys = [key for key, _ in simple_trie.items(explore_key[:2])]
            keys_to_explore = [
                key for key in simple_trie_keys if explore_key[:2] == key[:2]
            ]
            assert set(explored_keys) == set(keys_to_explore)


@pytest.mark.parametrize(
    ("simple_tuple_trie", "simple_trie_keys"),
    [
        (data_in_test.TupleIntData.key_list, data_in_test.TupleIntData.key_list),
        (data_in_test.TupleStrData.key_list, data_in_test.TupleStrData.key_list),
    ],
    indirect=True,
)
def test_tuple_trie_extend_key(simple_tuple_trie, simple_trie_keys) -> None:
    """Test if TupleTrie.extend returns expedted list of keys"""
    for explore_key in simple_trie_keys:
        for _ in range(1, len(explore_key)):
            explored_keys = [key for key, _ in simple_tuple_trie.items(explore_key[:2])]
            keys_to_explore = [
                key for key in simple_trie_keys if explore_key[:2] == key[:2]
            ]
            assert set(explored_keys) == set(keys_to_explore)
