"""
Core classes for retrie library.

This module contains the core classes for the retrie library, including the `BaseNode`
and `Node`, `BaseTrie`, `Trie` and `TupleTrie` classes. A trie is data structure for fast
lookup of many string patterns in a string. Trie objects in this library have similar
behavior to dict objects.  This is how it is used:

```python
from retrie import Trie
trie = Trie()
trie["hello"] = "Hola"
trie["world"] = "Mundo"
trie["hello world"] = "Hola Mundo"
trie["Python"] = "Python"
print(trie["hello"]) # Output: Hola

search_sequence = "hello world of Python"

print(list(trie.match(search_sequence))) 
# Output: [(5, 'Hola'), (11, 'Hola Mundo')]

print(list(trie.search(search_sequence))) 
# Output: [(0, 5, 'Hola'), (0, 11, 'Hola Mundo'), (6, 11, 'Mundo'), (15, 21, 'Python')]
```

You can also use TupleTrie for other sequence types:

```python
from retrie import TupleTrie
trie = TupleTrie()
trie[(1, 2, 3)] = "One Two Three" # with tuple paranthesis
trie[1, 2] = "One Two" # or without tuple paranthesis
trie[1, 3] = "One Three"

search_sequence = (1, 2, 1, 2, 3)

print(list(trie.match(search_sequence)))
# Output: [(2, 'One Two')]

print(list(trie.search(search_sequence)))
# Output: [(0, 2, 'One Two'), (2, 4, 'One Two'), (2, 5, 'One Two Three')]
```
"""
from collections import UserDict
from functools import reduce
from typing import Any, Iterable, Optional, TypeVar

from retrie.utils import pairwise

# constant values used in data structure
Empty = object()
NotDefined = object()
TrieKey = TypeVar("TrieKey", str, tuple)
TrieType = TypeVar("TrieType", bound="BaseTrie")

class BaseNode(dict):
    """
    Base class for Trie nodes.

    It is a dictlike object used for each nore of trie objets.
    """

    def __init__(self, value: Any=Empty) -> None:  ## Node TODO not exactly a dict
        self.value = value

    def setdefault(self, key:TrieKey, default: Any=None) -> Any:
        """
        If key is in the dictionary, return its value.

        If not, insert key with a value of default and return default.

        Args:
        key: The key to retrieve or add.
        default: The value to insert if key is not in the dictionary.
            If default is not provided, default is None.
        """
        return (
            self[key]
            if key in self
            else dict.setdefault(
                self,
                key,
                default() if callable(default) else default,
            )
        )


class Node(BaseNode):
    """
    Main class for nodes in Trie structure.

    It is a dict-like object used for each node of trie objects.
    """

    __slots__ = ("value",)

    def copy(self) -> BaseNode:
        """
        Create a shallow copy of the current Node instance.

        Returns:
            Node: A new Node instance that is a shallow copy of the current instance.
        """
        inst = self.__class__.__new__(self.__class__)
        inst.update(self)
        return inst


class BaseTrie(UserDict):
    """
    Base class for Trie data structures.

    This is a dictionary-like class which stores keys and values in a tree-like
    structure, allowing for efficient retrieval of values based on prefix
    matching of keys.
    """

    _length = 0

    def __init__(
        self,
        _dict: Optional[dict]=None,
        /,
        **kwargs: dict[TrieKey, Any],
    ) -> None:
        """
        Initialize a new instance of Trie or its subclasses.

        Args:
            _dict (dict, optional): An optional dictionary to initialize the trie with.
                For populating the object, you can use either _dict or
                pass it as kwargs.
            **kwargs: Additional keyword arguments to initialize the trie with.

        Returns:
        None
        """
        self.data = self.__newnode__()
        if _dict:
            self.update(_dict)
        if kwargs:
            self.update(kwargs)

    @staticmethod
    def __newnode__(item: Optional[Any]=Empty) -> Node:
        """
        Create and return a new Node instance.

        You can override it in subclasses to customize the behavior

        Args:
            item (Any, optional): The value to be stored in the new node.
                Defaults to Empty, which represents an empty node.

        Returns:
        Node: A new Node instance initialized with the given item.
        """
        return Node(item)

    def __setitem__(self, key: TrieKey, value: Any) -> None:
        """
        Set a value for a given key in the trie.

        This method tries to have a dict-like behavior.

        Args:
        key : Some iterable like str or tuple. Each item inside this iterable
        should be a hashable object.
        value : Any
            The value to be stored at the location specified by the key.

        Returns:
        None
        """
        current_node = self.data
        for item in key:
            current_node = current_node.setdefault(
                item,
                self.__newnode__,
            )  # TODO for every navigation step __newnode__ is called
        if current_node.value is Empty:
            self._length += 1
        current_node.value = value

    def __getitem__(self, key: TrieKey) -> Any:
        """
        Retrieve the value associated with a given key in the trie.

        Args:
        key (Iterable): The key to retrieve the value for. It should be an iterable
            like str or tuple, where each item inside this iterable
            should be a hashable object.

        Returns:
        value: The value associated with the given key in the trie.
            If the key is not found, a KeyError will be raised.
        """
        current_node = self.__getnode__(key)
        return current_node.value

    def __delitem__(self, key: TrieKey) -> None:
        """
        Remove a key-value pair from the trie.

        Args:
            key (Iterable): The key to be removed from the trie. It should be an
                iterable (e.g., string or tuple) where each item is a hashable object.

        Raises:
            KeyError: If the key is not found in the trie or if the key is empty.

        Returns:
            None
        """
        if not key or key not in self:
            raise KeyError("Key not found in trie object")

        keys = [(0, self.data), *self._traverse_nodes(key, only_leafs=False)]
        _, node = keys[-1]
        node.value = Empty
        self._length -= 1
        for (curr_key_len, curr_node), (prev_key_len, prev_node) in pairwise( #noqa
            keys[::-1],
        ):
            if len(curr_node) == 0 and curr_node.value is Empty:
                del prev_node[key[curr_key_len - 1]]
            else:
                break

    def __missing__(self, key: TrieKey) -> Any:
        """
        Handle the case when a key is not found in the Trie.

        This method is called when accessing a key not found in the Trie.

        Args:
            key (Iterable): The key that was not found in the Trie.

        Raises:
            KeyError: Always raised with a message indicating the missing key.

        Returns:
            Default value for the missing key
        """
        raise KeyError(f"Key {key} is missing in Trie")

    def __getnode_safe__(self, key: TrieKey) -> BaseNode:
        """
        Safely retrieve a node from trie for the key, return None if key is missing.

        This method traverses the trie structure following the given key,
        returning the final node if the key exists, or None if any part
        of the key is not found.

        Args:
            key (Iterable): An iterable (string or tuple) representing
                        the path to the desired node in the trie.

        Returns:
            Node or None: The node corresponding to the given key if it exists
                      in the trie, or None if any part of the key is not found.
        """
        try:
            current_node = self.data
            for letter in key:
                current_node = current_node[letter]
            return current_node
        except KeyError:
            return None

    def __getnode__(self, key: TrieKey, only_leafs: bool=True) -> BaseNode:
        """
        Retrieve a node in the trie for a given key.

        If key is not in the trie, it tries to call __missing__(key)
        for default value (which raises KeyError).

        Args:
            key (Iterable): The key to retrieve or create a node for.
            only_leafs (bool, optional): If True, only consider leaf nodes (nodes
             with values) as valid. Defaults to True.

        Returns:
            Node: The node corresponding to the given key.
        """
        current_node = self.__getnode_safe__(key)

        if current_node is None:
            newvalue = self.__missing__(key)
            self.__setitem__(key=key, value=newvalue)
            return self.__getnode__(key, only_leafs=True)

        if current_node.value is Empty and only_leafs:
            newvalue = self.__missing__(key)
            current_node.value = newvalue
            return current_node

        return current_node

    def __contains__(self, key: TrieKey) -> bool:
        """
        Check if key exists in the trie.

        Args:
            key: String to look up

        Returns:
            bool: True if key exists, False otherwise
        """
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def items(
        self,
        root_path: Optional[TrieKey]="",
    ) -> Iterable[tuple[TrieKey, Any]]:
        """
        Iterate over all (key, value) pairs in the trie.

        Yields:
            tuple: (key, value) pairs for all items in the trie
        """
        if root_path == "":
            root_node = self.data
        else:
            root_node = self.__getnode__(root_path, only_leafs=False)
        stack = [
            (root_path, root_node),
        ]

        while stack:
            path, node = stack.pop()
            if node.value is not Empty:
                yield path, node.value
            for key, child in node.items():
                stack.append(
                    [path + key, child],
                )

    __items__ = items

    def __iter__(self) -> Iterable[TrieKey]:
        """
        Iterate over all keys in the trie.

        Yields:
            tuple: keys in the trie
        """
        for key, _ in self.__items__():
            yield key

    def __repr__(self) -> str:
        return f'{{{", ".join(f"{key!r}: {val!r}" for key, val in self.items())}}}'

    def count(self) -> int:
        """
        Compute and return the number of items in the trie object.

        Returns:
            int: keys in the trie
        """
        self._length = reduce(lambda cnt, _: cnt + 1, self.items(), 0)
        return self._length

    def __len__(self) -> int:
        return self._length

    def copy(self) -> TrieType:
        """
        Create a shallow copy of the current Trie instance.

        Returns
            Trie: A new Trie instance that is a shallow copy of the current instance.
        """
        inst = self.__class__()
        for k, v in self.items():
            inst[k] = v
        return inst

    __copy__ = copy

    def _traverse_nodes(
        self,
        path: TrieKey,
        only_leafs: bool=True,
    ) -> Iterable[tuple[int, Node]]:
        """
        Traverse the trie structure following the given path.

        Yields:
            (int, node) for i as length of matched key and node object
        """
        if not path:
            yield 0, None
            return

        current_node = self.data

        for i, letter in enumerate(path):
            current_node = current_node.get(letter, None)
            if current_node is None:
                break
            if current_node.value is not Empty or not only_leafs:
                yield i + 1, current_node

    def match(self, path: TrieKey) -> Iterable[tuple[int, Any]]:
        """
        Traverse the trie structure following the given path.

        Yields:
            (int, node) for i as length of matched key and value for matched key
        """
        for length, node in self._traverse_nodes(path, only_leafs=True):
            yield length, node.value

    def search(self, text: TrieKey) -> Iterable[tuple[int, int, Any]]:
        """
        Search for all matches of keys in the given text.

        Keys can start from any position in the text.

        Yields:
            (int, int, Any) as (key start index, key end index, value for matched key)
        """
        for i in range(len(text)):
            for length, value in self.match(text[i:]):
                yield i, i + length, value


class StringTrie(BaseTrie):
    """
    A Trie data structure for storing string keys.

    It has similar insertion, insertion, and deletion behavior like a dictionary object.
    It also supports matching keys (which start from 0 in text) and also searching
    for any keys present in the text.
    """

    def to_regex(self) -> str:
        """
        Generate regex pattern to match keys in the trie object.

        Returns:
            str: Regex pattern to match keys in the trie object.
        """
        return self._regex(self.data)

    def _regex(self, node: Node, root_node: bool=True) -> str:
        """
        Generate regex pattern for specified node and it's childs.

        This method is used internal and called recursively on each node
        to generate regex patterns.

        Returns:
            str: Regex pattern to match keys in the trie object.
        """
        if not len(node) or node.value is not Empty:
            return ""

        inner_patterns = []
        terminal_keys = []
        childs = [
            (key, self._regex(ch_node, root_node=False))
            for key, ch_node in node.items()
        ]

        terminal_keys = [key for key, ch_pattern in childs if ch_pattern == ""]

        inner_patterns = [
            key + ch_pattern for key, ch_pattern in childs if ch_pattern != ""
        ]
        empty_inner_patterns = len(inner_patterns) == 0

        if len(terminal_keys) == 1:
            inner_patterns.append(terminal_keys[0])
        elif len(terminal_keys) > 1:
            inner_patterns.append("[" + "".join(terminal_keys) + "]")

        if len(inner_patterns) == 1:
            result = inner_patterns[0]
        elif root_node:
            result = "|".join(sorted(inner_patterns))
        else:
            result = "(?:" + "|".join(sorted(inner_patterns)) + ")"

        if node.value is not Empty and not root_node:
            if empty_inner_patterns:
                result += "?"
            else:
                result = "(?:" + result + ")?"

        return result


class TupleTrie(BaseTrie):
    """
    A Trie data structure for storing tuple keys.

    It has similar behavior to StringTries, but treats keys as tuples instead
    of strings.
    """

    def items(self, root_path: tuple=()) -> Iterable[tuple[tuple, Any]]:
        """
        Iterate over all (key, value) pairs in the TupleTrie object.

        keys are supposed to be tuples.

        Yields:
            tuple: (key, value) pairs for all items in the trie
        """
        if len(root_path) == 0:
            root_node = self.data
        else:
            root_node = self.__getnode__(root_path, only_leafs=False)
        stack = [
            (tuple(root_path), root_node),
        ]

        while stack:
            path, node = stack.pop()
            if node.value is not Empty:
                yield path, node.value
            for key, child in node.items():
                stack.append(
                    [ (*path, key), child],
                )


Trie = StringTrie
