import socket
import threading
import json



from Database import Database

class Coordinator:
    def __init__(self, host, port, database: Database):
        self.host = host
        self.port = port
        self.db = database
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(50)
        print(f"Coordinator listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, client_address):
        try:
            print("handling in thread")

            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    print("no message")
                    continue

                if message == '/connect':
                    client_socket.sendall('ack'.encode('utf-8'))
                    files_info = client_socket.recv(1024).decode('utf-8')
                    self.db.add_client(client_address, json.loads(files_info))
                    print(f"Client added to db {client_address}")
                    print(self.db.get_all_data())
                elif message == "/search_by_name":
                    pass
                elif message == "/search_by_md5":
                    pass
                elif message == "/search_by_name_md5":
                    pass
                elif message == "/get_owner_of_segment":
                    pass
                elif message == "/update_client":
                    pass
                elif message == '/close':
                    print(f"Closing connection with {client_address}")
                    break
        finally:
            client_socket.close()
            self.db.remove_client(client_address)
            print(f"Connection with {client_address} closed.")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connected with {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    coordinator = Coordinator('127.0.0.1', 65432, Database())
    coordinator.start()

