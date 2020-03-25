# First party
from mpu.datastructures.trie.string_trie import Trie


def test_trie_print():
    data = ["dog", "cat", "cattle", "tom", "d", "tomcat", "tomatoe"]
    trie = Trie(data)
    trie_data = trie.print(print_stdout=True)
    trie_data = trie.print(print_stdout=False)
    expected = """Trie
 cat
  tle
 d
  og
 tom
  atoe
  cat"""
    assert trie_data == expected
    trie.print(print_stdout=True)


def test_trie_creation_prefix_search():
    data = ["dog", "cat", "cattle", "tom", "d", "tomcat", "tomatoe"]
    trie = Trie(data)
    expected = set(["tom", "tomcat", "tomatoe"])
    prefix, subtrie = trie.get_subtrie("tom")
    assert set(prefix + element for element in subtrie) == expected


def test_get_subtrie_direct_hit2():
    trie = Trie(["foobar"])
    assert [word for subtrie in trie.get_subtrie("foobar") for word in subtrie] == [
        "foobar"
    ]
