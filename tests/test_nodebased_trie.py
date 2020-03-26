# Third party
import pytest

# First party
from mpu.datastructures.trie.char_trie import EMPTY_NODE as CHAR_EMPTY_NODE
from mpu.datastructures.trie.char_trie import Trie as CharTrie
from mpu.datastructures.trie.char_trie import TrieNode as CharTrieNode
from mpu.datastructures.trie.string_trie import EMPTY_NODE as STRING_EMPTY_NODE
from mpu.datastructures.trie.string_trie import Trie as StringTrie
from mpu.datastructures.trie.string_trie import TrieNode as StringTrieNode

nodebased_tries = [CharTrie, StringTrie]
nodebased_tries_empty_nodes = [
    (CharTrie, CHAR_EMPTY_NODE),
    (StringTrie, STRING_EMPTY_NODE),
]


@pytest.mark.parametrize("Trie,EMPTY_NODE", nodebased_tries_empty_nodes)
def test_get_subtrie_prefix_hit_miss(Trie, EMPTY_NODE):
    trie = Trie(["foo"])
    prefix, subtrie = trie.get_subtrie("foobar")
    assert subtrie is EMPTY_NODE


@pytest.mark.parametrize("Trie", nodebased_tries)
def test_get_subtrie_prefix_hit_hit(Trie):
    trie = Trie(["foo", "foobar"])
    words = []
    prefix, subtrie = trie.get_subtrie("foobar")
    for word in subtrie:
        words.append(prefix + word)
    assert words == ["foobar"]


@pytest.mark.parametrize("Trie,EMPTY_NODE", nodebased_tries_empty_nodes)
def test_get_subtrie_direct_miss(Trie, EMPTY_NODE):
    trie = Trie(["foo"])
    prefix, subtrie = trie.get_subtrie("bar")
    assert subtrie is EMPTY_NODE


@pytest.mark.parametrize("Trie", nodebased_tries)
def test_trie_autocomplete(Trie):
    data = ["dog", "cat", "cattle", "tom", "d", "tomcat", "tomatoe"]
    trie = Trie(data)
    assert list(trie.autocomplete("d")) == ["d", "dog"]
    expected = ["tom", "tomatoe", "tomcat"]
    assert sorted(list(trie.autocomplete("tom"))) == expected

    data = ["tom", "d"]
    trie = Trie(data)
    assert list(trie.autocomplete("t")) == ["tom"]

    data = ["dog", "tomco", "cat", "cattle", "tom", "d", "tomcat", "tomatoe"]
    trie = Trie(data)
    assert sorted(list(trie.autocomplete("tomc"))) == ["tomcat", "tomco"]
    trie.print()
    print(trie.get_subtrie("tom"))
    assert list(trie.autocomplete("x")) == []


@pytest.mark.parametrize("Trie", nodebased_tries)
def test_get_subtrie_direct_hit(Trie):
    trie = Trie(["foobar"])
    prefix, subtrie = trie.get_subtrie("foobar")
    assert [prefix + word for word in subtrie] == ["foobar"]


@pytest.mark.parametrize("Trie", nodebased_tries)
def test_get_subtrie_empty(Trie):
    trie = Trie()
    prefix, subtrie = trie.get_subtrie("foobar")
    assert prefix == ""
    assert not subtrie.is_word
    assert subtrie.count == 0


@pytest.mark.parametrize("Trie", nodebased_tries)
def test_trie_creation_prefix_search(Trie):
    data = ["dog", "cat", "cattle", "tom", "d", "tomcat", "tomatoe"]
    trie = Trie(data)
    expected = set(["tom", "tomcat", "tomatoe"])
    prefix, subtrie = trie.get_subtrie("tom")
    assert set(prefix + element for element in subtrie) == expected


@pytest.mark.parametrize("TrieNode", [CharTrieNode, StringTrieNode])
def test_frozen_node_push(TrieNode):
    node = TrieNode("a", freeze=True)
    with pytest.raises(RuntimeError):
        node.push("b")


@pytest.mark.parametrize("Trie", nodebased_tries)
def test_push_empty(Trie):
    trie = Trie()
    trie.push("")
