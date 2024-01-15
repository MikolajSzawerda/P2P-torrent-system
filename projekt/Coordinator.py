import socket
import threading
import json

class Coordinator:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(50)
        print(f"Coordinator listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, client_address):
        try:
            print("handling in thread")

            while True:
                message = client_socket.recv(1024).decode('utf-8')
                client_socket.sendall('ack'.encode('utf-8'))
                if not message:
                    print("no message")
                    continue

                if message == '/connect':
                    files_info = client_socket.recv(1024).decode('utf-8')
                    self.clients[client_address] = json.loads(files_info)
                    print(f"Client {client_address} connected with files: {self.clients[client_address]}")
                elif message == '/close':
                    print(f"Closing connection with {client_address}")
                    break
        finally:
            client_socket.close()
            del self.clients[client_address]
            print(f"Connection with {client_address} closed.")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connected with {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    coordinator = Coordinator('127.0.0.1', 65432)
    coordinator.start()
