# Core Library
from abc import ABCMeta, abstractmethod


class ListNode(metaclass=ABCMeta):
    def __init__(self, value):
        """Every list node should have a value at initialization."""

    @property
    @abstractmethod
    def value(self):
        """Read the value attribute"""

    @property
    @abstractmethod
    def next(self):
        """Read the next attribute"""

    @next.setter
    def next(self, next_):
        """Write the next attribute"""


class SinglyLinkedListNode(ListNode):
    def __init__(self, value):
        self._value = value
        self._next = None  # Optional[SinglyLinkedListNode]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next_):
        self._next = next_


def reverse(list_node: ListNode) -> ListNode:
    """Reverse a list."""
    current = list_node
    previous = None

    while current is not None:
        previous, current.next, current = current, previous, current.next

    return previous
