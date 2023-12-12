import socket
import struct

from linked_list import Node
from config import FIXED_SIZE_STRING_LENGTH


def serialize_list(node: Node) -> bytes:
    data = b''

    while node:
        data += struct.pack("i", node.data_type)

        if node.data_type == 0:
            data += struct.pack("h", node.data)
        elif node.data_type == 1:
            data += struct.pack("i", node.data)
        elif node.data_type == 2:
            data += struct.pack(f"{FIXED_SIZE_STRING_LENGTH}s", node.data.encode("utf-8"))
        else:
            data += struct.pack(f"{len(node.data) + 1}s", node.data.encode("utf-8"))

        node = node.next

    return data

def main():
    head = Node(0, 123)
    head.next = Node(1, 456)
    head.next.next = Node(2, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    head.next.next.next = Node(3, "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8080))

    data = serialize_list(head)

    s.sendall(data)


if __name__ == '__main__':
    main()
