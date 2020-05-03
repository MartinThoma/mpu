#!/usr/bin/env python

"""Test the mpu.datastructures.char_trie module."""

# Third party
import pytest

# First party
from mpu.datastructures.trie.char_trie import EMPTY_NODE, Trie, TrieNode


def test_trie_print():
    data = ["dog", "cat", "cattle", "tom", "d", "tomcat", "tomatoe"]
    trie = Trie(data)
    trie_data = trie.print(print_stdout=False)
    expected = """Trie

 c
  a
   t
    t
     l
      e
 d
  o
   g
 t
  o
   m
    a
     t
      o
       e
    c
     a
      t"""
    assert trie_data == expected
    trie.print(print_stdout=True)


def test_create_trie_node_with_children():
    TrieNode("b", children={"a": TrieNode("a")})


def test_trie_node_push():
    node = TrieNode(value="a")
    with pytest.raises(ValueError):
        node.push("")


def test_get_subtrie_from_empty():
    node = Trie()
    prefix, node = node.get_subtrie("")
    assert prefix == ""
    assert node._value == EMPTY_NODE._value
    assert node.is_word == EMPTY_NODE.is_word
    assert node.count == EMPTY_NODE.count
    assert node.children == EMPTY_NODE.children
