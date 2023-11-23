import socket
import sys
from shared_tools import prepare_message, get_alphanet_message

HOST = '127.0.0.1'


def send_udp_message(message: bytes, host: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message, (host, port))
        data = sock.recv(len(message))
        print('Received: {}'.format(data))




if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 8000
    print("using port: ", port)

    msg = get_alphanet_message(200)
    encoded_msg = prepare_message(msg)
    send_udp_message(encoded_msg, HOST, port)