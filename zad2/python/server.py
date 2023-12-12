import socket
import struct

from linked_list import Node
from config import HOST, PORT, FIXED_SIZE_STRING_LENGTH, BUFF_SIZE, NODES_COUNT


def deserialize_list(data: bytes) -> Node:
    head = None
    current_node = None
    i = 0
    nodes_cnt = 0

    while nodes_cnt < NODES_COUNT and i < len(data):
        data_type = struct.unpack('i', data[i:i+4])[0]
        i += 4

        if data_type == 0:
            content = struct.unpack('h', data[i:i+2])[0]
            i += 2
        elif data_type == 1:
            content = struct.unpack('i', data[i:i+4])[0]
            i += 4
        elif data_type == 2:
            content = struct.unpack(f'{FIXED_SIZE_STRING_LENGTH}s', data[i:i+FIXED_SIZE_STRING_LENGTH])[0]
            content = content.decode('utf-8')
            i += FIXED_SIZE_STRING_LENGTH
        else:
            j = i
            while data[j] != 0:
                j += 1

            content = struct.unpack(f'{j-i+1}s', data[i:j+1])[0].decode('utf-8')

            i = j+1

        if current_node is None:
            current_node = Node(data_type, content)
            head = current_node
        else:
            current_node.next = Node(data_type, content)
            current_node = current_node.next

        nodes_cnt += 1

    return head


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((HOST, PORT))

    s.listen(1)

    client_socket, _ = s.accept()

    data = client_socket.recv(BUFF_SIZE)

    head = deserialize_list(data)
    head.display()


if __name__ == "__main__":
    main()
