#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the mpu.datastructures.char_trie module."""

# First party
from mpu.datastructures.trie.char_trie import Trie


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
