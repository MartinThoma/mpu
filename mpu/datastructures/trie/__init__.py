"""
A trie is a prefix-tree. It allows efficient search by prefixes.

There are three different prefix-trees implemented in mpu:

* FullPrefixTrie: Every prefix of every word is stored
* CharTrie: Every single character is a node
* StringTrie: Every node stores a substring of the word which is as long as
  possible.

|                               | FullPrefixTrie | CharTrie | StringTrie |
| ----------------------------- | -------------- | -------- | ---------- |
| Insert word with w characters | O(w)           | O(w)     | ?          |
| Lookup word with w characters | O(1)           | O(w)     | ?          |

Typically, the FullPrefixTrie is the fastest solution and uses by far most
memory.

See also
--------
* [Should a prefix tree (trie) node store only a single character or a
  string?](https://cs.stackexchange.com/q/121937/2914)
"""

# First party
from mpu.datastructures.trie.char_trie import Trie as CharTrie  # noqa
from mpu.datastructures.trie.full_prefix_dict import FullPrefixDict  # noqa
from mpu.datastructures.trie.string_trie import Trie as StringTrie  # noqa

Trie = FullPrefixDict
