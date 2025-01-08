"""
A simple implementation of Radix algorithm.

A Radix is a memory efficient version of a Trie data structure.
All feaures avaible in Trie (StringTrie) are supported by Radix objects.
"""
from collections import UserDict
from collections.abc import Iterable
from typing import Any
from typing import Optional
from typing import Tuple

from sortedcollections import SortedList

from triematch.trie import Empty
from triematch.trie import Node
from triematch.trie import NotDefined
from triematch.trie import Trie
from triematch.trie import TrieKey
from triematch.utils import pairwise


class RadixNode(Node):
    """A Node elelemnt used in Radix data structures."""

    __slots__ = (*Node.__slots__, 'key_list')

    def __init__(self, value: Any=Empty) -> None:
        """
        Construct a new Radix Node with the given value.

        Args:
            value (Any, optional): The value associated with this node. Default
            is `Empty` object.
        """
        self.value = value
        self.key_list = SortedList()

    def __setitem__(self, __key: Any, __value: Any) -> None:
        """Set the value associated with this node."""
        if __key not in self.key_list:
            self.key_list.add(__key)
        super().__setitem__(__key, __value)

    __marker = object()

    def pop(self, key: str, default: Optional[Any]=NotDefined) -> Any:
        """Remove the subkey from the node and return the value."""
        try:
            value = self[key]
        except KeyError:
            if default is NotDefined:
                raise
            return default
        else:
            del self[key]
            return value

    def __delitem__(self, __key: Any) -> None:
        """Remove the key and its corresponding value from the node."""
        super().__delitem__(__key)
        self.key_list.remove(__key)

def argmax(items: Iterable[Any]) -> Any:
    """Find the index of the item with the maximum value."""
    max_value = -1 ## all values are positive numbers
    max_index = -1
    i = 0
    for item in items:
        if item > max_value:
            max_value = item
            max_index = i
        i += 1
    return max_index


def common_start(key: str) -> callable:
    """
    Return a wrapper which looks for common length.

    Common length is the length of common part (from index 0) between
    key and the key passed to the wrapper.
    """
    key_len = len(key)

    def wrapper(nb_key: str) -> str:
        common_len = min(len(nb_key), key_len)
        for i in range(common_len):
            if nb_key[i] == key[i]:
                continue
            return i
        return common_len

    return wrapper


class Radix(Trie):
    """
    Radix data structure.

    This class is a simple implementation of Radix data structure, which is a
    memory efficient version of a Trie.
    """

    trie = None

    @staticmethod
    def __newnode__(item: Optional[Any]=Empty) -> Any:
        return RadixNode(item)

    def __setitem__(self, key: str, value: Any) -> None:
        current_node = self.data
        found_path_len = 0
        while found_path_len < len(key):

            closest_key, common_part_len = self.candidate_key(
                current_node,
                key[found_path_len:],
            )

            if not closest_key or common_part_len < len(closest_key):
                break

            if common_part_len == len(closest_key):
                current_node = current_node[closest_key]
                found_path_len += len(closest_key)
                continue
        else:
            ## the whole key exists in radix, update it's node

            if current_node.value is Empty:
                self._length += 1
            current_node.value = value
            return

        remaining_key = key[found_path_len:]
        try:
            # check if there is a partial subkey of the key remaning
            subkey, subcommon_part = self.candidate_key(current_node, remaining_key)

            if not subcommon_part:
                ##  no part of remaining_key exists in trie
                new_node = self.__newnode__()
                new_node.value = value
                current_node[remaining_key] = new_node  # assign it to current node
                self._length += 1
                return

            common_subkey = subkey[:subcommon_part]
            rest_subkey = subkey[subcommon_part:]
            rest_remaining_key = remaining_key[subcommon_part:]
            current_node[common_subkey] = self.__newnode__()
            current_node[common_subkey][rest_subkey] = current_node.pop(subkey)

            if rest_remaining_key:
                current_node[common_subkey][rest_remaining_key] = self.__newnode__(
                    value,
                )
            else:
                current_node[common_subkey].value = value
            self._length += 1
        except KeyError:
            raise

    def __getnode__(self, key: str, only_leafs: bool=True) -> RadixNode:
        """Retrieve the node associated with a given key in the Radix tree."""
        current_node = self.data
        found_path_len = 0
        while found_path_len < len(key):
            key_cand, common_len = self.candidate_key(
                current_node,
                key[found_path_len:],
            )
            if common_len and common_len == len(key_cand):
                current_node = current_node[key_cand]
                found_path_len += len(key_cand)
            else:
                break

        # if current_node.value is Empty and only_leafs:
        if found_path_len < len(key) or \
            (current_node.value is Empty and not only_leafs):
            return self.__missing__(key)

        return current_node

    def _regex(self, node: RadixNode, root_node: bool=True) -> str:
        if not len(node) or node.value is not Empty:
            return ''

        inner_patterns = []
        terminal_keys = []
        childs = [
            (key, self._regex(ch_node, False))
            for key, ch_node in node.items()
        ]

        terminal_keys = [
            key
            for key, ch_pattern in childs
            if ch_pattern == ''
        ]

        inner_patterns = [
            key + ch_pattern
            for key, ch_pattern in childs
            if ch_pattern != ''
        ]
        empty_inner_patterns = len(inner_patterns) == 0


        if len(terminal_keys) == 1:
            inner_patterns.append(terminal_keys[0])
        elif len(terminal_keys) > 1:
            if root_node:
                inner_patterns.append('|'.join(sorted(terminal_keys)))
            elif max(map(len, terminal_keys)) == 1:
                inner_patterns.append('[' + ''.join(sorted(terminal_keys)) + ']')
            else:
                inner_patterns.append('(?:' + '|'.join(sorted(terminal_keys)) + ')')

        if len(inner_patterns) == 1:
            result = inner_patterns[0]
        elif len(inner_patterns) > 1 and inner_patterns:
            if root_node:
                result = '|'.join(sorted(inner_patterns))
            else:
                result = '(?:' + '|'.join(sorted(inner_patterns)) + ')'

        if node.value is not Empty:
            result = '?' if empty_inner_patterns else f'(?:{result})?'

        return result

    def __delitem__(self, key: str) -> None:
        if not key or key not in self:
            raise KeyError('Key not found in trie object')

        keys = [(0, self.data), *self._traverse_nodes(key, only_leafs=False)]
        _, node = keys[-1]
        node.value = Empty
        self._length -= 1
        for (curr_key_len, curr_node), (prev_key_len, prev_node) in pairwise(
            keys[::-1],
        ):
            if len(curr_node) == 0 and curr_node.value is Empty:
                del prev_node[key[prev_key_len:curr_key_len]]
                ## TODO update key??
            elif len(curr_node) == 1 and curr_node.value is Empty:
                ((next_skey, next_node),) = (*curr_node.items(),)
                curr_skey = key[prev_key_len:curr_key_len]
                new_skey = curr_skey + next_skey
                prev_node[new_skey] = next_node
                del prev_node[curr_skey]
                break
            else:
                break

    def candidate_key(self, node: RadixNode, key: str) -> tuple[str, int]:
        """
        Find most similar keys to given subkey based on node structure.

        Retruns the key which can be a candidate for splitting and
        sharing with new key inserted to the tree.
        """
        if not len(node.key_list):
            return None, 0
        index = node.key_list.bisect_left(key)
        if index == 0:
            nearby_keys = node.key_list[:1]
        else:
            nearby_keys = node.key_list[index - 1 : index + 1]
        common_parts = list(map(common_start(key), nearby_keys))
        idx = argmax(common_parts)
        return nearby_keys[idx], common_parts[idx]

    def _traverse_nodes(
        self,
        path: str,
        only_leafs: bool=True,
    ) -> Iterable[tuple[int, RadixNode]]:
        if not path:
            yield 0, None
            return
        return_all = not only_leafs

        current_node = self.data if isinstance(self, UserDict) else self

        curr_index = 0
        current_node = self.data
        while curr_index < len(path):
            key_cand, common_len = self.candidate_key(current_node, path[curr_index:])
            if common_len and common_len == len(key_cand):
                current_node = current_node[key_cand]
                curr_index += len(key_cand)
                if current_node.value is not Empty or return_all:
                    yield curr_index, current_node
            else:
                break

    def expand(self, path: TrieKey) -> Iterable[tuple[int, Any]]:
        """
        Look for patterns which contains `path` key.

        Yields:
            (int, node) for i as length of matched key and value for matched key
        """
        path_len = len(path)

        current_node = self.data
        found_path_len = 0

        while found_path_len < path_len:
            key_cand, common_len = self.candidate_key(
                current_node,
                path[found_path_len:],
            )
            if common_len and common_len == len(key_cand):
                current_node = current_node[key_cand]
                found_path_len += len(key_cand)
            else:
                break

        if found_path_len < path_len:
            remaining_key = path[found_path_len:]

            idx = current_node.key_list.bisect_left(remaining_key)
            curr_nodes = []
            for key in current_node.key_list[idx:]:
                if not key.startswith(remaining_key):
                    break
                curr_nodes.append((remaining_key, current_node[key]))
        else:
            curr_nodes = [(path_len, current_node)]

        for remain_key, node in curr_nodes:
            node_path = path + remain_key
            yield from ((node_path + ext, node) for ext, node in node.explore())
