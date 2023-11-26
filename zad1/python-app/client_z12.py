import socket
import sys
from msg_tools import prepare_proper_message
from config import BUFSIZE, PORT, INFO_MSG, HOST

def send_udp_message(message: bytes, host: str, port: int) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message, (host, port))
        data = sock.recv(BUFSIZE)
    return data

def find_max_datagram_size(host: str, port: int) -> None:
    max_size = 1020
    try:
        while True:
            msg = prepare_proper_message(max_size)
            data = send_udp_message(msg, host, port)
            print(f"Sent {max_size} bytes")

            if data.decode('utf-8') == INFO_MSG:
                max_size += 1
            else:
                break
    except KeyboardInterrupt:
        pass

    print(f"Maximum datagram size: {max_size - 1} bytes")

if __name__ == "__main__":
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except:
        host = HOST
        port = PORT

    print(f"Finding maximum datagram size on {host}:{port}")

    find_max_datagram_size(host, port)


# Maksymalny rozmiar datagramu wynoszący 1024 bajty w tym przypadku wynika z ograniczeń związanych z konfiguracją bufora używanego do odbierania danych w programie serwera.