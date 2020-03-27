# First party
from mpu.datastructures.lists import SinglyLinkedListNode, reverse


def test_node_creation():
    node1 = SinglyLinkedListNode("foobar")
    assert node1.value == "foobar"
    assert node1.next is None

    node2 = SinglyLinkedListNode("test")
    node1.next = node2

    assert node1.next.value == "test"


def test_reverse():
    node1 = SinglyLinkedListNode("a")
    node2 = SinglyLinkedListNode("b")
    node3 = SinglyLinkedListNode("c")
    node4 = SinglyLinkedListNode("d")

    node1.next = node2
    node2.next = node3
    node3.next = node4

    assert node1.value == "a"
    assert node1.next.value == "b"
    assert node1.next.next.value == "c"
    assert node1.next.next.next.value == "d"

    reversed_list = reverse(node1)
    assert reversed_list.value == "d"
    assert reversed_list.next.value == "c"
    assert reversed_list.next.next.value == "b"
    assert reversed_list.next.next.next.value == "a"
