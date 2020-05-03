# Core Library
import logging
from typing import Dict, List, Tuple

# First party
from mpu.datastructures.trie.base import AbstractTrie

logger = logging.getLogger(__name__)


class TrieNode:
    def __init__(self, value, is_word=False, count=0, children=None, freeze=False):
        if children is None:
            children = dict()
        self._value = value
        self.children: Dict[str, TrieNode] = children
        self.is_word = is_word
        self.count = count
        self.is_frozen = freeze

    def get_subtrie(self, search_prefix: str, current_trie_node_prefix: str = ""):
        """
        Get the TrieNodes which represents the given prefix.

        If the search_prefix is not in the trie, return ("", EMPTY_NODE).
        The found_prefix is a prefix of search_prefix or equal to it.

        Parameters
        ----------
        search_prefix : str
        current_trie_node_prefix : str, optional (default: "")

        Returns
        -------
        found_prefix, subtrie: Tuple[str, TrieNode]
        """
        if len(search_prefix) == 0:
            return (current_trie_node_prefix, self)
        elif search_prefix[0] in self.children:
            child = self.children[search_prefix[0]]
            remainder = search_prefix[1:]
            new_prefix = current_trie_node_prefix + self._value
            return child.get_subtrie(remainder, current_trie_node_prefix=new_prefix)
        else:
            return ("", EMPTY_NODE)

    def push(self, value: str):
        if self.is_frozen:
            raise RuntimeError("The node is frozen. You may not edit it.")
        if value == self._value and len(value) == 0:
            # This is the root node
            self.is_word = True
            self.count += 1
            return
        if len(value) == 0:
            raise ValueError("The pushed value should not be empty")
        elif len(value) == 1:
            char = value[0]
            if char not in self.children:
                self.children[char] = TrieNode(value=char, is_word=True, count=1)
            else:
                self.children[char].is_word = True
                self.children[char].count += 1
        else:
            char = value[0]
            if char not in self.children:
                self.children[char] = TrieNode(value=char, is_word=False, count=0)
            self.children[char].push(value[1:])

    def __iter__(self):
        self._iteration_queue: List[TrieNode, str] = [(self, "")]
        while self._iteration_queue:
            trie_node, prefix = self._iteration_queue.pop()
            children = sorted(trie_node.children.items(), key=lambda n: n[0])
            for _, child in children:
                self._iteration_queue.append((child, prefix + trie_node._value))
            if trie_node.is_word:
                for _ in range(trie_node.count):
                    yield prefix + trie_node._value

    def print(self, _indent: int = 0):
        string = ""
        string += " " * _indent + self._value + "\n"
        children = sorted(self.children.values(), key=lambda child: child._value)
        for child in children:
            string += child.print(_indent=_indent + 1)
        return string

    def __str__(self):
        return (
            f"TrieNode(value='{self._value}', " f"nb_children='{len(self.children)}')"
        )

    __repr__ = __str__


EMPTY_NODE = TrieNode(value="", is_word=False, count=0, freeze=True)


class Trie(AbstractTrie):
    def __init__(self, container=None):
        if container is None:
            container = []
        self._root = TrieNode(value="", count=0, is_word=0)
        self._length = 0
        for element in container:
            self.push(element)

    def __len__(self):
        return self._length

    def __contains__(self, element) -> bool:
        found_prefix, subtrie = self.get_subtrie(element)
        return subtrie.is_word and found_prefix + subtrie._value == element

    def autocomplete(self, prefix):
        found_prefix, subtrie = self.get_subtrie(prefix)
        for word in subtrie:
            yield found_prefix + word

    def get_subtrie(self, prefix) -> Tuple[str, TrieNode]:
        return self._root.get_subtrie(prefix)

    def __iter__(self):
        self._iteration_index = -1
        self._child_values = [element for element in self._root]
        return self

    def __next__(self):
        """Return the next value from the Trie."""
        self._iteration_index += 1
        if self._iteration_index < self._length:
            return self._child_values[self._iteration_index]
        raise StopIteration

    def push(self, element: str):
        self._root.push(element)
        self._length += 1

    def print(self, print_stdout=True) -> str:
        string = "Trie\n"
        string += self._root.print()
        string = string.strip()
        if print_stdout:
            print(string)
        return string

    def __str__(self):
        return f"Trie(len={self._length}, {self._root})"

    __repr__ = __str__
