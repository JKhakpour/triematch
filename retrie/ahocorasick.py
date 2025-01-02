"""
Classes for Aho-Corasick Trie and related items.

Classes:
- ACTrieStates
- ACNode
- ACTrie

"""
from collections import deque
from enum import Enum
from typing import Any, Iterable, Optional

from .trie import Empty, Node, StringTrie


class ACTrieStates(Enum):
    """Enum for Aho-Corasick Trie states."""

    Not_Linked = 1
    Linked = 2


class ACNode(Node):
    """
    A node in the Aho-Corasick Automaton.

    These objects are used in Aho-Corasick Trie structure.
    """

    __slots__ = ("value", "dict_link", "failure_link", "pathlen")

    def __init__(self, value: Any=Empty) -> None:
        """
        Construct ACNode instance.

        Args:
            value (Any, optional): The value associated with this node.
            Default value is `Empty` object.
        """
        self.value = value
        self.dict_link = None
        self.failure_link = Empty
        self.pathlen = None

class ACTrie(StringTrie):
    """
    Aho-Corasick Trie data structure.

    This class has a behavior similar to StringTrie. When ACTrie.link_nodes is called,
    The trie would generate links between nodes to speedup search. After calling
    ACTrie.link_nodes, Trie would not allow modifications, untless you run unlink_nodes
    and just use it like a normal StringTrie.
    """

    mode = False
    _state = ACTrieStates.Not_Linked

    def __init__(self, _dict: Optional[dict]=None, /, **kwargs: dict[str, Any]) -> None:
        super().__init__(_dict, **kwargs)
        self.data.failure_link = (
            self.data
        )  # root node is self referencing for failure case

    @staticmethod
    def __newnode__(item: Optional[Any]=Empty) -> ACNode:
        return ACNode(item)

    def _update_failure_links(self) -> None:
        root_node = self.data
        root_node.failure_link = root_node
        root_node.pathlen = -1
        stack = deque(
            (root_node, transition, child) for transition, child in root_node.items()
        )

        while stack:
            parent, transition_path, node = stack.pop()
            ref = parent
            # while transition not in ref.failure_link and ref is not root_node:
            #     ref = ref.failure_link
            tr_path_len = len(transition_path)
            for i in range(1, tr_path_len):
                link = self.__getnode_safe__(transition_path[i:])

                if link is not None:
                    node.failure_link = link
                    break
            else:
                node.failure_link = root_node
            node.pathlen = ref.pathlen + 1

            for transition, child in node.items():
                stack.appendleft((node, transition_path + transition, child))

    def _update_dict_links(self) -> None:
        root_node = self.data
        stack = deque()
        stack.appendleft(root_node)
        while stack:
            node = stack.pop()
            ref = node.failure_link
            while ref.value is Empty and ref is not root_node:
                ref = ref.failure_link

            if ref is not root_node:
                node.dict_link = ref

            for child_node in node.values():
                stack.appendleft(child_node)

    def _check_update_possible(self) -> None:
        if self._state == ACTrieStates.Linked:
            raise AttributeError("Not possible!")

    def __setitem__(self, key: str, value: Any) -> None:
        self._check_update_possible()
        current_node = self.data
        for item in key:
            current_node = current_node.setdefault(
                item,
                self.__newnode__,
            )  # TODO for ever navigation step __newnode__ is called
        if current_node.value is Empty:
            self._length += 1
        current_node.value = value

    def __delitem__(self, key: str) -> None:
        self._check_update_possible()
        if self._state == ACTrieStates.Linked:
            raise AttributeError("Not possible!")
        return super().__delitem__(key)

    def link_nodes(self) -> None:
        """Generate lookup links between nodes and freeze the tree."""
        self._update_failure_links()
        self._update_dict_links()
        self._state = ACTrieStates.Linked

    def unlink_nodes(self) -> None:
        """
        Allow modification on ACTrie.

        If this method is called, the ACTrie will search for
        patterns like a regular Trie.
        """
        self._state = ACTrieStates.Not_Linked

    def search(self, text: str) -> Iterable[Any]:
        """
        Search for the patterns in the given text.

        If link_nodes is called, this methid will use failure and dictionary links
        to speed up the search process. In other cases it will work as a regular Trie.

        Args:
            text (str): The text to search for patterns.
        """
        if self._state != ACTrieStates.Linked:
            yield from super().search(text)
            return
        if not text:
            yield 0, 0, None
            return

        root_node = current_node = self.data

        for i, letter in enumerate(text):
            while letter not in current_node and current_node is not root_node:
                current_node = current_node.failure_link

            current_node = current_node.get(letter, root_node)
            if current_node.value is not Empty:
                yield (
                    i - current_node.pathlen, i + 1, current_node.value,
                )

            value_node = current_node
            while True:
                value_node = value_node.dict_link
                if value_node is None:
                    break
                yield i - value_node.pathlen, i + 1, value_node.value
