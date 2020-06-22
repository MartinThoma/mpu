# Core Library
import logging
from typing import List, Set, Tuple

# First party
from mpu.datastructures.trie.base import AbstractTrie

logger = logging.getLogger(__name__)


class TrieNode:
    def __init__(self, value, is_word=False, count=0, children=None, freeze=False):
        if children is None:
            children = set()
        self._value = value
        self.children: Set[TrieNode] = children
        self.is_word = is_word
        self.count = count
        self.is_frozen = freeze

    def get_subtrie(
        self, search_prefix: str, current_trie_node_prefix: str = ""
    ) -> Tuple[str, "TrieNode"]:
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
        if search_prefix == self._value[: len(search_prefix)]:
            # search_prefix is a prefix of the current node (or equal to it)
            return (current_trie_node_prefix, self)
        elif self._value == search_prefix[: len(self._value)]:
            # The current node is a prefix of the search_prefix
            remainder = search_prefix[len(self._value) :]
            children = sorted(self.children, key=lambda node: node._value)
            for child in children:
                if child._value == remainder[: len(child._value)]:
                    new_prefix = current_trie_node_prefix + self._value
                    return child.get_subtrie(
                        remainder, current_trie_node_prefix=new_prefix
                    )
                elif remainder == child._value[: len(remainder)]:
                    # The remainder is a prefix of the child
                    return (current_trie_node_prefix, child)
        return ("", EMPTY_NODE)

    def push(self, value: str):
        if self.is_frozen:
            raise RuntimeError("The node is frozen. You may not edit it.")
        if value == self._value:
            logger.debug("The inserted value is the value of the current node")
            self.count += 1
            self.is_word = True
            return
        shared_prefix = get_shared_prefix(self._value, value)

        if len(value) == len(shared_prefix):
            logger.debug("The new value is a prefix of the current node")
            new_child = TrieNode(
                self._value[len(shared_prefix) :],
                is_word=self.is_word,
                count=self.count,
                children=self.children,
            )
            self._value = shared_prefix
            self.count = 1
            self.is_word = True
            self.children = {new_child}
        elif len(shared_prefix) == len(self._value):
            logger.debug(
                f"The current node={self._value} is a prefix "
                f"of the new value={value}"
            )
            # Do I have a child which also is a prefix of this?
            remainder = value[len(shared_prefix) :]
            for child_trie in self.children:
                if len(get_shared_prefix(child_trie._value, remainder)) > 0:
                    child_trie.push(remainder)
                    return
            trie_node = TrieNode(value[len(shared_prefix) :], is_word=True, count=1)
            self.children.add(trie_node)
        else:
            logger.debug(f"No shared prefix for {self._value} and {value}")
            # Current node willl become its child
            old_data = TrieNode(
                self._value[len(shared_prefix) :],
                is_word=self.is_word,
                count=self.count,
                children=self.children,
            )

            # New data
            new_data = TrieNode(value[len(shared_prefix) :], is_word=True, count=1)

            # Clean up current node
            self.is_word = False
            self.count = 0
            self._value = shared_prefix
            self.children = {old_data, new_data}

    def __iter__(self):
        self._iteration_queue: List[TrieNode, str] = [(self, "")]
        while self._iteration_queue:
            trie_node, prefix = self._iteration_queue.pop()
            for child in trie_node.children:
                self._iteration_queue.append((child, prefix + trie_node._value))
            if trie_node.is_word:
                for _ in range(trie_node.count):
                    yield prefix + trie_node._value

    def print(self, _indent: int = 0):
        string = ""
        if self.is_word:
            string += " " * _indent + self._value + "\n"
        children = sorted(self.children, key=lambda child: child._value)
        for i, child in enumerate(children):
            if i < len(self.children) - 1:
                string += child.print(_indent=_indent + 1)
            else:
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
        self._root = None
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

    def get_subtrie(
        self, prefix
    ) -> Tuple[str, TrieNode]:  # TODO: Should this be private?
        if self._root is None:
            return ("", EMPTY_NODE)
        return self._root.get_subtrie(prefix)

    def __iter__(self):
        self._iteration_index = -1
        self._child_values = []
        if self._root is not None:
            self._child_values = [element for element in self._root]
        return self

    def __next__(self):
        """Return the next value from the Trie."""
        self._iteration_index += 1
        if self._iteration_index < self._length:
            return self._child_values[self._iteration_index]
        raise StopIteration

    def push(self, element: str):
        if self._root is None:
            self._root = TrieNode(value=element, is_word=True, count=1)
        else:
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


def get_shared_prefix(word1: str, word2: str) -> str:
    """
    Get the substring in the beginning of word1 and word2 which both share.

    Parameters
    ----------
    word1 : str
    word2 : str

    Returns
    -------
    shared_prefix : str

    Examples
    --------
    >>> get_shared_prefix("foo", "bar")
    ''
    >>> get_shared_prefix("foobar", "bar")
    ''
    >>> get_shared_prefix("foobar", "foo")
    'foo'
    >>> get_shared_prefix("steamship", "steampowered")
    'steam'
    """
    shared_prefix = ""
    for char1, char2 in zip(word1, word2):
        if char1 == char2:
            shared_prefix += char1
        else:
            break
    return shared_prefix
