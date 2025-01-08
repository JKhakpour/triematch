"""Data used by tests cases and pytest fixtures are stored here."""

class StrData:
    """Parameters used in testing string key based Tries are stored in this class."""

    new_key: str = 'afgh'  # this key is added to trie later
    long_key: str = 'dabdab'  # a long key
    missing_key: str = 'xyz'  # this key is missing in trie
    # keys of a trie, keep it immutable because it is
    # passed as default param to a function
    key_list = ('aaa', 'abc', 'abcd', 'abed', long_key)

class TupleStrData:
    """Parameters used in testing (tuple of strings) key based Tries"""

    new_key = ('asd', 'abc')  # this key is added to trie later
    long_key = ('dd', 'aaa', 'bb', 'dd', 'ab')  # a long key
    missing_key = ('x', 'yz')  # this key is missing in trie
    key_list = (
        ('aa', 'bb', 'cc'),
        ('aa', 'bb', 'dd'),
        ('aaa', 'bbb', 'ccc'),
        long_key,
    )


class TupleIntData:
    """Parameters used in testing (tuple of strings) key based Tries"""

    new_key = (11, 5)  # this key is added to trie later
    long_key = (1, 2, 3, 4, 5)  # a long key
    missing_key = (1, 8)  # this key is missing in trie
    explore_root = (11, 22)
    key_list = (
        (11, 22, 33),
        (11, 22, 444),
        (111, 222, 333),
        long_key,
    )


class ALLTypes:
    """
    Combination of all above data parameter clases for different types.
    Used for parameterized tests
    """

    new_keys = (
        StrData.new_key,
        TupleStrData.new_key,
        TupleIntData.new_key,
    )
    long_keys = (
        StrData.long_key,
        TupleStrData.long_key,
        TupleIntData.long_key,
    )
    missing_keys = (
        StrData.missing_key,
        TupleStrData.missing_key,
        TupleIntData.missing_key,
    )
    key_lists = (
        StrData.key_list,
        TupleStrData.key_list,
        TupleIntData.key_list,
    )


Etc = ...
