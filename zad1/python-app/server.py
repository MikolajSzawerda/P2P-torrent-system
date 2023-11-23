import socket
import sys
from msg_tools import verify_message
from config import HOST, BUFSIZE, INFO_MSG, ERROR_MSG, PORT

def serve_udp(host: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        while True:
            data, address = s.recvfrom(BUFSIZE)
            print(f"received: {data}")

            if verify_message(data):
                s.sendto(INFO_MSG.encode(), address)
            else:
                s.sendto(ERROR_MSG.encode(), address)


if __name__ == "__main__":
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except:
        host = HOST
        port = PORT

    print(f"listening on {host}:{port}")

    serve_udp(host, port)