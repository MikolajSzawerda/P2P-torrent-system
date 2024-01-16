import socket
import threading
import json

from Database import Database, FileFormatException


class ExitClient(Exception):
    pass


class Coordinator:
    def __init__(self, host, port, database: Database):
        self.host = host
        self.port = port
        self.db = database
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(50)
        print(f"Coordinator listening on {self.host}:{self.port}")

    def disconnect_client(self, client_socket, client_address):
        client_socket.close()
        self.db.remove_client(client_address)
        print(f"Connection with {client_address} closed.")

    def handle_message(self, message, client_socket, client_address):
        action = message[:20]

        if action.startswith('/connect'):
            payload = json.loads(message[20:])
            try:
                self.db.add_client(client_address, payload["files"])
                print(f"Client added to db {client_address}")
            except FileFormatException as e:
                client_socket.sendall(str(e).encode("utf-8"))
                print(f"Failed connect attempt of {client_address}")
                raise ExitClient()
            print(self.db.get_all_data())
            client_socket.sendall("success".encode("utf-8"))
        elif action == "/search_by_name":
            pass
        elif action == "/search_by_md5":
            pass
        elif action == "/search_by_name_md5":
            pass
        elif action == "/get_owner_of_segment":
            pass
        elif action == "/update_client":
            pass
        elif action.startswith('/close'):
            print(f"Closing connection with {client_address}")
            raise ExitClient()

    def handle_client(self, client_socket, client_address):
        try:

            while True:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    print("no message")
                    continue

                try:
                    self.handle_message(message, client_socket, client_address)
                except ExitClient:
                    break

        finally:
            self.disconnect_client(client_socket, client_address)

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connected with {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    coordinator = Coordinator('127.0.0.1', 65432, Database())
    coordinator.start()
