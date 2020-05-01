#!/usr/bin/env python

"""Test the mpu.datastructures.char_trie module."""

# Third party
import pytest

# First party
from mpu.datastructures.trie.char_trie import Trie, TrieNode


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
