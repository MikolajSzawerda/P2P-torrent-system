import socket
import threading
import json
from time import sleep

from coordinator.src.database import Database, FileFormatException


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
        action = message[:30]


        if action.startswith('/connect'):
            try:
                payload = json.loads(message[30:])
                self.db.add_client(client_address, payload["files"])
                print(f"Client added to db {client_address}")
                client_socket.sendall("success".encode("utf-8"))
            except FileFormatException as e:
                client_socket.sendall(str(e).encode("utf-8"))
                print(f"Failed connect attempt of {client_address}")
                raise ExitClient()
            # print(self.db.get_all_data())
        elif action.startswith("/search_by_name"):
            payload = json.loads(message[30:])
            files = self.db.get_files_by_name(payload["name"])
            client_socket.sendall(json.dumps(files).encode("utf-8"))
        elif action.startswith("/search_by_md5"):
            payload = json.loads(message[30:])
            files = self.db.get_files_by_md5(payload["md5"])
            client_socket.sendall(json.dumps(files).encode("utf-8"))
        elif action.startswith("/search_by_name_md5"):
            payload = json.loads(message[30:])
            files = self.db.get_files_by_name_and_md5(payload["name"], payload["md5"])
            client_socket.sendall(json.dumps(files).encode("utf-8"))
        elif action.startswith("/get_owner_of_segment"):
            payload = json.loads(message[30:])
            client = self.db.get_client_with_file(payload["name"], payload["md5"], payload["segment_number"])
            client_socket.sendall(json.dumps(client).encode("utf-8"))
        elif action.startswith("/update_client"):
            payload = json.loads(message[30:])
            self.db.add_client(client_address, payload["files"])
            client_socket.sendall("success".encode("utf-8"))
        elif action.startswith('/close'):
            print(f"Closing connection with {client_address}")
            raise ExitClient()
        else:
            print("cannot handle")

    def handle_client(self, client_socket, client_address):
        try:

            while True:
                message = client_socket.recv(1024).decode("utf-8")
                if not message:
                    print("no message")
                    sleep(0.05)
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
