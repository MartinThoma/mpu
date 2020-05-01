# Core Library
from collections import defaultdict

# First party
from mpu.datastructures.trie.base import AbstractTrie


class FullPrefixDict(AbstractTrie):
    def __init__(self, container=None):
        if container is None:
            container = []
        self._prefix2words = defaultdict(list)  # Prefix to list of words
        self._len = 0
        for element in container:
            self.push(element)

    def __len__(self):
        return self._len

    def __iter__(self):
        yield from self._prefix2words[""]

    def push(self, element):
        self._len += 1
        for i in range(0, len(element) + 1):
            prefix = element[:i]
            self._prefix2words[prefix].append(element)
            self._prefix2words[prefix] = sorted(self._prefix2words[prefix])

    def autocomplete(self, prefix):
        return self._prefix2words[prefix]

    def __contains__(self, element):
        return element in self._prefix2words[element]
