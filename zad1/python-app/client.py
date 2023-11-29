import socket
import sys
import select

from msg_tools import prepare_proper_message, prepare_other_content_message, prepare_other_length_message
from config import BUFSIZE, PORT

HOST = '127.0.0.1'

BASE_TIMOUT = 1
MAX_TIMEOUT = 8
TIMEOUT_DECAY = 2


def send_udp_message(
        message: bytes,
        host: str,
        port: int,
        timeout: int = BASE_TIMOUT,
) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setblocking(0)
        sock.sendto(message, (host, port))

        ready, _, _ = select.select([sock], [], [], timeout)

        if not ready:
            new_timeout = timeout * TIMEOUT_DECAY if timeout * TIMEOUT_DECAY <= MAX_TIMEOUT else timeout
            print(f"Package not received, retrying with timeout {new_timeout}s...")
            return send_udp_message(message, host, port, new_timeout)

        data = sock.recv(BUFSIZE)

        print('Received: {}'.format(data))


if __name__ == "__main__":
    try:
        num = int(sys.argv[1])
        host = sys.argv[2]
        port = int(sys.argv[3])
        case = int(sys.argv[4]) # 1 - proper message, 2 - other content, 3 - other length
    except:
        num = 200
        host = HOST
        port = PORT
        case = 1

    print(f"Sending {num} bytes to {host}:{port}, case {case}")

    if case == 1:
        msg = prepare_proper_message(num)
    elif case == 2:
        msg = prepare_other_content_message(num)
    elif case == 3:
        msg = prepare_other_length_message(num)
    else:
        raise ValueError('case must be 1, 2 or 3')

    send_udp_message(msg, HOST, port)