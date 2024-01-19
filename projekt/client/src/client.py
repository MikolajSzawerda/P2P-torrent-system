import socket
import json
from time import sleep


class Client:
    def __init__(self, coordinator_host, coordinator_port):
        self.coordinator_host = coordinator_host
        self.coordinator_port = coordinator_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def format_message(self, action, payload):
        action += " " * (30 - len(action))
        return action + payload

    def connect_and_send_files(self, files_info):
        self.client_socket.connect((self.coordinator_host, self.coordinator_port))
        print(
            f"Connected to Coordinator at {self.coordinator_host}:{self.coordinator_port}"
        )
        msg = self.format_message("/connect", json.dumps(files_info))
        print(msg)
        self.client_socket.sendall(msg.encode("utf-8"))
        result = self.client_socket.recv(1024).decode("utf-8")
        print(result)

    def search_by_name(self, name):
        msg = self.format_message("/search_by_name", json.dumps({"name": name}))
        self.client_socket.sendall(msg.encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(response)

    def search_by_md5(self, md5):
        msg = self.format_message("/search_by_md5", json.dumps({"md5": md5}))
        self.client_socket.sendall(msg.encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(response)

    def search_by_name_and_md5(self, name, md5):
        msg = self.format_message(
            "/search_by_name_md5", json.dumps({"name": name, "md5": md5})
        )
        self.client_socket.sendall(msg.encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(response)

    def get_owner_of_segment(self, name, md5, segment_number):
        msg = self.format_message(
            "/get_owner_of_segment",
            json.dumps({"name": name, "md5": md5, "segment_number": segment_number}),
        )
        self.client_socket.sendall(msg.encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(response)

    def update_client(self, files_info):
        msg = self.format_message("/update_client", json.dumps({"files": files_info}))
        self.client_socket.sendall(msg.encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(response)

    def close_connection(self):
        self.client_socket.sendall("/close".encode("utf-8"))
        self.client_socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    client = Client("127.0.0.1", 65432)
    client.client_socket.connect(("127.0.0.1", 65432))
    client.client_socket.sendall(
        json.dumps(
            {
                "route": "connect",
                "payload": {
                    "files": [
                        {"name": "a.txt", "hash": "123", "size": 1231},
                        {"name": "b.txt", "hash": "456", "size": 123},
                        {"name": "c.txt", "hash": "789", "size": 123},
                    ]
                },
            }
        ).encode()
    )

    response = client.client_socket.recv(1024).decode("utf-8")
    print(response)

    client.client_socket.sendall(
        json.dumps(
            {
                "route": "share_file",
                "payload": {"file": {"name": "d.txt", "hash": "xyz", "size": 1231}},
            }
        ).encode()
    )

    response = client.client_socket.recv(1024).decode("utf-8")
    print(response)

    client.client_socket.sendall(
        json.dumps({"route": "search_by_name", "payload": {"name": "a.txt"}}).encode()
    )

    response = client.client_socket.recv(1024).decode("utf-8")
    print(response)

    client.client_socket.sendall(
        json.dumps(
            {
                "route": "assign_segments",
                "payload": {"name": "a.txt", "hash": "123", "segment_ids": [0, 1]},
            }
        ).encode()
    )

    response = client.client_socket.recv(1024).decode("utf-8")
    print(response)

    # generate stats
    client.client_socket.sendall(
        json.dumps({"route": "generate_stats", "payload": {}}).encode()
    )
    response = client.client_socket.recv(1024).decode("utf-8")
    print(response)
    # while True:
    #     pass

    client.client_socket.close()
